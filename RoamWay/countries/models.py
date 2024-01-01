import django.db.models

from users.models import User


__all__ = []


class AbstractCountryModel(django.db.models.Model):
    name = django.db.models.CharField(
        max_length=128,
        verbose_name="название страны",
    )
    iso = django.db.models.CharField(
        max_length=2,
        verbose_name="iso-код страны",
    )

    class Meta:
        abstract = True


class Country(AbstractCountryModel):
    pass

    class Meta:
        verbose_name = "страна"
        verbose_name_plural = "страны"


class UserDesiredCountry(AbstractCountryModel):
    pass

    class Meta:
        verbose_name = "желаемая для посещения страна"
        verbose_name_plural = "желаемые для посещения страны"


class UserVisitedCountry(AbstractCountryModel):
    date_visited = django.db.models.DateTimeField(
        auto_now_add=True,
        null=True,
        blank=True,
        verbose_name="дата посещения",
    )

    class Meta:
        verbose_name = "посещенная страна"
        verbose_name_plural = "посещенные страны"


class CountryTask(django.db.models.Model):
    text = django.db.models.TextField(
        verbose_name="текст задачи",
    )
    country = django.db.models.ForeignKey(
        Country,
        on_delete=django.db.models.CASCADE,
        related_name="tasks",
    )
    user = django.db.models.ForeignKey(
        User,
        on_delete=django.db.models.CASCADE,
        related_name="tasks",
    )

    class Meta:
        verbose_name = "задача для страны"
        verbose_name_plural = "задачи для стран"
