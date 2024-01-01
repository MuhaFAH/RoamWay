from django.urls import path

import countries.views
import homepage.views

app_name = "homepage"

urlpatterns = [
    path(
        "",
        homepage.views.main,
        name="main",
    ),
    path(
        "photos/",
        homepage.views.photos,
        name="photos",
    ),
    path(
        "map/",
        homepage.views.map_,
        name="map",
    ),
    path(
        "about/",
        homepage.views.about,
        name="about",
    ),
    path(
        "tasks/",
        countries.views.tasks,
        name="tasks",
    ),
    path(
        "delete_photo/<int:photo_id>/",
        homepage.views.delete_photo,
        name="delete_photo",
    ),
]
