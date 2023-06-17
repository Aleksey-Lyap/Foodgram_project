from django.contrib import admin
from .models import User, Follow


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_filter = ('username', 'email')
    list_display = ('username', 'email', 'id')

admin.site.register(Follow)
