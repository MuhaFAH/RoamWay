from django.contrib.auth.models import User
import django.db.models

from countries import models
import users.constants
import users.managers

__all__ = []


class Profile(django.db.models.Model):
    user = django.db.models.OneToOneField(
        User,
        on_delete=django.db.models.CASCADE,
        related_name="profile",
        related_query_name="profile",
    )
    image = django.db.models.ImageField(
        blank=True,
        null=True,
        upload_to="users/avatars/",
        verbose_name="аватарка",
    )
    visited_countries_count = django.db.models.PositiveIntegerField(
        default=0,
        verbose_name="стран посещено",
    )
    homeland_country = django.db.models.CharField(
        max_length=255,
        verbose_name="родная страна",
        default="",
        choices=users.constants.COUNTRIES,
    )
    roamway_link = django.db.models.CharField(
        max_length=255,
        verbose_name="ссылка на аккаунт RoamWay",
        default="",
    )
    twitter_link = django.db.models.CharField(
        max_length=255,
        verbose_name="ссылка на аккаунт Twitter",
        default="",
    )
    instagram_link = django.db.models.CharField(
        max_length=255,
        verbose_name="ссылка на аккаунт Instagram",
        default="",
    )
    facebook_link = django.db.models.CharField(
        max_length=255,
        verbose_name="ссылка на аккаунт Facebook",
        default="",
    )
    visited_countries = django.db.models.ManyToManyField(
        models.UserVisitedCountry,
        related_name="visited_countries",
        related_query_name="visited_countries",
        blank=True,
    )
    desired_countries = django.db.models.ManyToManyField(
        models.UserDesiredCountry,
        related_name="desired_countries",
        related_query_name="desired_countries",
        blank=True,
    )

    class Meta:
        verbose_name = "Дополнительное поле"
        verbose_name_plural = "Дополнительные поля"


class User(User):
    objects = users.managers.UserManager()

    class Meta:
        proxy = True
        verbose_name = "пользователь"
        verbose_name_plural = "пользователи"


class UserUploadedFiles(django.db.models.Model):
    def create_path(self, filename):
        return f"uploads/{self.user_id}/{filename}"

    file = django.db.models.FileField(
        upload_to=create_path,
        verbose_name="файл",
    )

    user = django.db.models.ForeignKey(
        User,
        on_delete=django.db.models.CASCADE,
        related_name="files",
        related_query_name="files",
    )
