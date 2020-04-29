from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Office, Person

User = get_user_model()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "last_login", "is_active", "is_superuser", "office"]
    search_fields = ["username"]


@admin.register(Office)
class OfficeAdmin(admin.ModelAdmin):
    list_display = ["id", "name"]
    search_fields = ["id", "name"]
