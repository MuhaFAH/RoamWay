from django.urls import path

import countries.views

app_name = "countries"

urlpatterns = [
    path(
        "add_to_visited/<str:iso>/",
        countries.views.add_to_visited,
        name="add_to_visited",
    ),
    path(
        "add_to_wish_list/<str:iso>/",
        countries.views.add_to_wish_list,
        name="add_to_wish_list",
    ),
    path(
        "remove_cntry_status/<str:iso>/",
        countries.views.remove_cntry_status,
        name="remove_cntry_status",
    ),
    path(
        "del_task/<int:pk>/",
        countries.views.del_task,
        name="del_task",
    ),
    path("add_new_task/", countries.views.add_new_task, name="new_task"),
]
