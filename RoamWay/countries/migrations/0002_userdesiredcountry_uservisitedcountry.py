# Generated by Django 4.2.5 on 2023-12-18 14:16

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("countries", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="UserDesiredCountry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, verbose_name="название страны"
                    ),
                ),
                (
                    "iso",
                    models.CharField(
                        max_length=2, verbose_name="iso-код страны"
                    ),
                ),
            ],
            options={
                "abstract": False,
            },
        ),
        migrations.CreateModel(
            name="UserVisitedCountry",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                (
                    "name",
                    models.CharField(
                        max_length=128, verbose_name="название страны"
                    ),
                ),
                (
                    "iso",
                    models.CharField(
                        max_length=2, verbose_name="iso-код страны"
                    ),
                ),
                ("date_visited", models.DateField()),
            ],
            options={
                "abstract": False,
            },
        ),
    ]