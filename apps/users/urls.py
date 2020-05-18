from django.urls import path

from apps.users.api.views import (
    ListPersonAPIView,
    PersonAPIView,
    registration_view
)

app_name = "users"

urlpatterns = [
    path("list/", ListPersonAPIView.as_view(), name='persons-list'),
    path("<slug:pk>/", PersonAPIView.as_view(), name='persons-detail'),
    path('register', registration_view, name='register'),
]
