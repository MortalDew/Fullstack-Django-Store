from django.urls import include, path

urlpatterns = []

urlpatterns += [
    path("catalog/", include("app.catalog.urls")),
]
