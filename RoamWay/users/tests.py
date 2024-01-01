from http import HTTPStatus

from django.contrib.auth.models import User
from django.core.signing import TimestampSigner
from django.shortcuts import reverse
from django.test import Client, TestCase
from freezegun import freeze_time
import parameterized.parameterized

from users.forms import RegisterForm

__all__ = []


class StaticURLTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.username_2 = "username_2"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"
        cls.signer = TimestampSigner()

    @parameterized.parameterized.expand(
        [
            (reverse("users:login"), HTTPStatus.OK),
            (reverse("users:signup"), HTTPStatus.OK),
        ],
    )
    def test_anonymous_users_endpoint(self, url, status):
        response = Client().get(url)
        self.assertEqual(response.status_code, status)

    def test_anonymous_and_logged_profile_endpoint(self):
        response = self.client.get(reverse("users:user_profile"))

        self.assertEqual(response.status_code, HTTPStatus.FOUND)

        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        signed_username = self.signer.sign(self.username)

        self.client.get(
            reverse(
                "users:activate",
                kwargs={"username": signed_username},
            ),
        )

        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.get(reverse("users:user_profile"))

        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.client.get(reverse("users:logout"))

        form_data = {
            "username": self.username_2,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        signed_username = self.signer.sign(self.username_2)

        self.client.get(
            reverse(
                "users:activate",
                kwargs={"username": signed_username},
            ),
        )

        self.assertIn("_auth_user_id", self.client.session)

        response = self.client.get(
            reverse("users:profile_by_id", kwargs={"profile_id": 1}),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)

        response = self.client.get(
            reverse("users:profile_by_id", kwargs={"profile_id": 2}),
        )

        self.assertEqual(response.status_code, HTTPStatus.OK)


class FormTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.client = Client()
        cls.form = RegisterForm

    def test_form_in_context(self):
        response = self.client.get(reverse("users:signup"))
        self.assertIn("form", response.context)

    def test_form_with_error_mail(self):
        form_data = {
            "email": "не мейл",
        }
        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "email",
            ["Введите правильный адрес электронной почты."],
        )

    def test_form_with_error_password_not_same(self):
        form_data = {
            "password1": "1_Dnho25dGG11",
            "password2": "1",
        }
        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "password2",
            ["Введенные пароли не совпадают."],
        )

    def test_form_with_error_empty_username(self):
        form_data = {"username": ""}
        form = RegisterForm(data=form_data)

        self.assertFalse(form.is_valid())
        self.assertFormError(
            form,
            "username",
            ["Обязательное поле."],
        )


class RegistrationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"

    def test_register_correct_user(self):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        users_count = User.objects.count()

        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                username=self.username,
            ).exists(),
        )


class UserActivationTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"
        cls.signer = TimestampSigner()

    def test_register_and_activate_correct_user(self):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        users_count = User.objects.count()

        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )

        signed_username = self.signer.sign(self.username)

        self.client.get(
            reverse(
                "users:activate",
                kwargs={"username": signed_username},
            ),
        )

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=True,
            ).exists(),
        )

    def test_error_activate_after_12_hours(self):
        form_data = {
            "username": self.username,
            "email": self.email,
            "password1": self.password1,
            "password2": self.password2,
        }

        users_count = User.objects.count()

        response = self.client.post(
            reverse("users:signup"),
            data=form_data,
            follow=True,
        )

        self.assertRedirects(response, reverse("users:login"))
        self.assertEqual(User.objects.count(), users_count + 1)
        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )

        signed_username = self.signer.sign(self.username)

        with freeze_time("2023-12-25"):
            self.client.get(
                reverse(
                    "users:activate",
                    kwargs={"username": signed_username},
                ),
            )

        self.assertTrue(
            User.objects.filter(
                username=self.username,
                is_active=False,
            ).exists(),
        )
