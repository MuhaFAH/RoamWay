from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render
from django.urls import reverse

from countries.forms import TaskCreateForm, TextForm
from countries.models import (
    Country,
    CountryTask,
    UserDesiredCountry,
    UserVisitedCountry,
)
from users.models import User

__all__ = []


@login_required
def add_to_visited(request, iso):
    try:
        cntry = Country.objects.get(iso=iso)
    except Country.DoesNotExist:
        return redirect(request.META.get("HTTP_REFERER"))

    visited_cntry, created = UserVisitedCountry.objects.update_or_create(
        name=cntry.name,
        iso=cntry.iso,
    )

    user = User.objects.get(id=request.user.id)

    try:
        desired_country = user.profile.desired_countries.get(iso=iso)
    except UserDesiredCountry.DoesNotExist:
        pass
    else:
        desired_country.delete()

    try:
        user.profile.visited_countries.get(iso=iso)
    except UserVisitedCountry.DoesNotExist:
        user.profile.visited_countries.add(visited_cntry)
        user.profile.visited_countries_count = (
            user.profile.visited_countries.count()
        )
        user.profile.save()

    try:
        return redirect(request.META.get("HTTP_REFERER"))
    except TypeError:
        return redirect(reverse("homepage:main"))


@login_required
def add_to_wish_list(request, iso):
    cntry = Country.objects.get(iso=iso)
    desired_cntry, _ = UserDesiredCountry.objects.update_or_create(
        name=cntry.name,
        iso=cntry.iso,
    )
    user = User.objects.get(id=request.user.id)

    try:
        visited_country = user.profile.visited_countries.get(iso=iso)
    except UserVisitedCountry.DoesNotExist:
        pass
    else:
        visited_country.delete()

    try:
        user.profile.desired_countries.get(iso=iso)
    except UserDesiredCountry.DoesNotExist:
        user.profile.desired_countries.add(desired_cntry)
        user.profile.visited_countries_count = (
            user.profile.visited_countries.count()
        )
        user.profile.save()

    try:
        return redirect(request.META.get("HTTP_REFERER"))
    except TypeError:
        return redirect(reverse("homepage:main"))


@login_required
def remove_cntry_status(request, iso):
    user = User.objects.get(id=request.user.id)

    try:
        visited_country = user.profile.visited_countries.get(iso=iso)
    except UserVisitedCountry.DoesNotExist:
        pass
    else:
        visited_country.delete()
        user.profile.visited_countries_count = (
            user.profile.visited_countries.count()
        )
        user.profile.save()

    try:
        desired_country = user.profile.desired_countries.get(iso=iso)
    except UserDesiredCountry.DoesNotExist:
        pass
    else:
        desired_country.delete()

    try:
        return redirect(request.META.get("HTTP_REFERER"))
    except TypeError:
        return redirect(reverse("homepage:main"))


@login_required
def tasks(request):
    template = "homepage/tasks.html"
    user = User.objects.get(id=request.user.id)
    tasks = CountryTask.objects.filter(user_id=user.pk)
    context = {
        "tasks": tasks,
    }
    return render(request, template, context)


@login_required
def add_new_task(request):
    template = "homepage/add_task.html"
    cntry_form = TaskCreateForm(request.POST or None)
    text_form = TextForm(request.POST or None)
    if request.method == "POST":
        if cntry_form.is_valid() and text_form.is_valid():
            country = Country.objects.get(
                name=cntry_form.cleaned_data["homeland_country"],
            )
            text = text_form.cleaned_data["text"]
            user = User.objects.get(id=request.user.id)
            country.tasks.create(text=text, user_id=user.pk)
            return redirect("homepage:tasks")
    context = {
        "cntry_form": cntry_form,
        "text_form": text_form,
    }
    return render(request, template, context)


@login_required
def del_task(request, pk):
    task = CountryTask.objects.get(id=pk)
    task.delete()
    return redirect(reverse("homepage:tasks"))
