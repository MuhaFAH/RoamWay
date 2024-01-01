# Generated by Django 4.2.5 on 2023-12-18 17:14

from django.db import migrations, models

__all__ = ["Migration"]


class Migration(migrations.Migration):
    dependencies = [
        ("countries", "0002_userdesiredcountry_uservisitedcountry"),
        ("users", "0003_alter_profile_desired_countries_and_more"),
    ]

    operations = [
        migrations.AlterField(
            model_name="profile",
            name="desired_countries",
            field=models.ManyToManyField(
                blank=True,
                related_name="desired_countries",
                to="countries.userdesiredcountry",
            ),
        ),
    ]
