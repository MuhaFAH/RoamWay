from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect, render, reverse

from users.forms import PhotosFileForm
from users.models import User, UserUploadedFiles

__all__ = []


@login_required
def main(request):
    template = "homepage/main.html"
    user = User.objects.get(id=request.user.id)

    users_images = (
        UserUploadedFiles.objects.select_related("user")
        .only(
            "file",
            "user",
        )
        .order_by("-id")[:2]
    )

    recommended_users = (
        User.objects.filter(is_active=True)
        .exclude(id=user.id)
        .order_by("?")[:4]
        .select_related("profile")
        .only("username", "profile", "id")
    )

    context = {
        "visited": user.profile.visited_countries.all(),
        "desired": user.profile.desired_countries.all(),
        "images": users_images,
        "recommended_users": recommended_users,
    }
    return render(request, template, context)


@login_required
def photos(request):
    template = "homepage/photos.html"
    files_form = PhotosFileForm(request.POST or None)

    if request.method == "POST":
        if "files" in request.FILES:
            from pathlib import Path

            for upload_file in request.FILES.getlist("files"):
                filename = Path(upload_file.name)
                extension = filename.suffix
                if extension != ".jpg" and extension != ".png":
                    messages.success(
                        request,
                        "Данный тип файла не поддерживается",
                    )
                else:
                    UserUploadedFiles.objects.create(
                        file=upload_file,
                        user=request.user,
                    )

    users_images = UserUploadedFiles.objects.select_related("user").only(
        "file",
        "user",
    )

    context = {
        "files_form": files_form,
        "images": users_images,
    }
    return render(request, template, context)


@login_required
def map_(request):
    template = "homepage/map.html"
    user = User.objects.get(id=request.user.id)
    context = {
        "visited": user.profile.visited_countries.all(),
        "desired": user.profile.desired_countries.all(),
    }
    return render(request, template, context)


def delete_photo(request, photo_id):
    photo = UserUploadedFiles.objects.filter(pk=photo_id).get()

    if request.user == photo.user:
        photo.delete()

    return redirect(reverse("homepage:photos"))


def about(request):
    template = "homepage/about.html"

    context = {}
    return render(request, template, context)
