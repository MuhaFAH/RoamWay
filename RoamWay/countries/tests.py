from http import HTTPStatus

from django.core.signing import TimestampSigner
from django.test import TestCase
from django.urls import reverse
import parameterized

from countries.models import Country

__all__ = []


class CountriesStatusTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"
        cls.signer = TimestampSigner()
        cls.country = Country.objects.create(
            name="France",
            iso="FR",
        )

    @parameterized.parameterized.expand(
        [
            (
                reverse("countries:add_to_visited", kwargs={"iso": "FR"}),
                HTTPStatus.FOUND,
            ),
            (
                reverse("countries:add_to_wish_list", kwargs={"iso": "FR"}),
                HTTPStatus.FOUND,
            ),
            (
                reverse("countries:remove_cntry_status", kwargs={"iso": "FR"}),
                HTTPStatus.FOUND,
            ),
        ],
    )
    def test_countries_anonymous_status_change(self, url, status):
        response = self.client.get(url)
        self.assertEqual(response.status_code, status)
        self.assertTrue(reverse("users:login") + "?next=" in response.url)

    @parameterized.parameterized.expand(
        [
            (
                reverse("countries:add_to_visited", kwargs={"iso": "FR"}),
                HTTPStatus.FOUND,
            ),
            (
                reverse("countries:add_to_wish_list", kwargs={"iso": "FR"}),
                HTTPStatus.FOUND,
            ),
            (
                reverse("countries:remove_cntry_status", kwargs={"iso": "FR"}),
                HTTPStatus.FOUND,
            ),
        ],
    )
    def test_countries_logged_status_change(self, url, status):
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
        response = self.client.get(url)
        self.assertEqual(response.status_code, status)
        self.assertRedirects(response, reverse("homepage:main"))
