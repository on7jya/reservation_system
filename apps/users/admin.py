from django.contrib import admin
from django.contrib.auth import get_user_model
from .models import Person

User = get_user_model()


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "last_login", "is_active", "is_superuser", "office"]
    search_fields = ["username"]
