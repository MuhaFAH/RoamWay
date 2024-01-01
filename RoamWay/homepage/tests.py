from http import HTTPStatus
import tempfile

from django.core.files.uploadedfile import SimpleUploadedFile
from django.core.signing import TimestampSigner
from django.test import Client, override_settings, TestCase
from django.urls import reverse
import parameterized

from users.models import UserUploadedFiles

__all__ = []


class StaticURLTests(TestCase):
    @parameterized.parameterized.expand(
        [
            (reverse("homepage:main"), HTTPStatus.FOUND),
            (reverse("homepage:map"), HTTPStatus.FOUND),
            (reverse("homepage:photos"), HTTPStatus.FOUND),
            (reverse("homepage:about"), HTTPStatus.OK),
        ],
    )
    def test_homepage_endpoint(self, url, status):
        response = Client().get(url)
        self.assertEqual(response.status_code, status)


class PhotoUploadTests(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        cls.username = "username"
        cls.email = "test@mail.ru"
        cls.password1 = "1_Dnho25dGG11"
        cls.password2 = "1_Dnho25dGG11"
        cls.signer = TimestampSigner()

    @override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory(prefix="uploads").name,
    )
    def test_upload_multiple_photos(self):
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

        form_data = {
            "files": [
                SimpleUploadedFile(
                    "test_img.jpg",
                    b"file_content",
                    content_type="image/jpeg",
                ),
                SimpleUploadedFile(
                    "test_img2.jpg",
                    b"file_content2",
                    content_type="image/jpeg",
                ),
            ],
        }

        response = self.client.post(
            reverse("homepage:photos"),
            data=form_data,
        )

        filename_1 = form_data["files"][0].name
        filename_2 = form_data["files"][1].name
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            UserUploadedFiles.objects.filter(
                file__exact=f"uploads/1/{filename_1}",
            ).exists(),
        )
        self.assertTrue(
            UserUploadedFiles.objects.filter(
                file__exact=f"uploads/1/{filename_2}",
            ).exists(),
        )

    @override_settings(
        MEDIA_ROOT=tempfile.TemporaryDirectory(prefix="uploads").name,
    )
    def test_upload_and_delete_multiple_photos(self):
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

        form_data = {
            "files": [
                SimpleUploadedFile(
                    "test_img.jpg",
                    b"file_content",
                    content_type="image/jpeg",
                ),
                SimpleUploadedFile(
                    "test_img2.jpg",
                    b"file_content2",
                    content_type="image/jpeg",
                ),
            ],
        }

        response = self.client.post(
            reverse("homepage:photos"),
            data=form_data,
        )

        filename_1 = form_data["files"][0].name
        filename_2 = form_data["files"][1].name
        self.assertEqual(response.status_code, HTTPStatus.OK)
        self.assertTrue(
            UserUploadedFiles.objects.filter(
                file__exact=f"uploads/1/{filename_1}",
            ).exists(),
        )
        self.assertTrue(
            UserUploadedFiles.objects.filter(
                file__exact=f"uploads/1/{filename_2}",
            ).exists(),
        )

        response = self.client.post(
            reverse("homepage:delete_photo", kwargs={"photo_id": 1}),
            follow=True,
        )

        self.assertRedirects(response, reverse("homepage:photos"))

        self.assertFalse(
            UserUploadedFiles.objects.filter(
                file__exact=f"uploads/1/{filename_1}",
            ).exists(),
        )

        response = self.client.post(
            reverse("homepage:delete_photo", kwargs={"photo_id": 2}),
            follow=True,
        )

        self.assertRedirects(response, reverse("homepage:photos"))

        self.assertFalse(
            UserUploadedFiles.objects.filter(
                file__exact=f"uploads/1/{filename_2}",
            ).exists(),
        )
