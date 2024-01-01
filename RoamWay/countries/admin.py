from django.contrib import admin

import countries.models

__all__ = []


@admin.register(countries.models.UserVisitedCountry)
class UserVisitedCountryAdmin(admin.ModelAdmin):
    list_display = (countries.models.UserVisitedCountry.name.field.name,)

    readonly_fields = [
        countries.models.UserVisitedCountry.name.field.name,
        countries.models.UserVisitedCountry.iso.field.name,
        countries.models.UserVisitedCountry.date_visited.field.name,
    ]


@admin.register(countries.models.UserDesiredCountry)
class UserDesiredCountryAdmin(admin.ModelAdmin):
    list_display = (countries.models.UserDesiredCountry.name.field.name,)

    readonly_fields = [
        countries.models.UserDesiredCountry.name.field.name,
        countries.models.UserDesiredCountry.iso.field.name,
    ]


@admin.register(countries.models.Country)
class CountryAdmin(admin.ModelAdmin):
    list_display = (countries.models.Country.name.field.name,)
