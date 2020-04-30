from django.contrib import admin
from .models import Person


@admin.register(Person)
class PersonAdmin(admin.ModelAdmin):
    list_display = ["username", "email", "last_login", "is_active", "is_superuser", "office"]
    search_fields = ["username"]
