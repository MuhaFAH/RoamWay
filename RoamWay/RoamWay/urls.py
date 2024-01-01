from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

import users.urls

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("homepage.urls")),
    path("countries/", include("countries.urls")),
    path("auth/", include(users.urls)),
    path("auth/", include("django.contrib.auth.urls")),
]

urlpatterns += static(
    settings.MEDIA_URL,
    document_root=settings.MEDIA_ROOT,
)

if settings.DEBUG:
    import debug_toolbar

    urlpatterns.append(path("__debug__/", include(debug_toolbar.urls)))
