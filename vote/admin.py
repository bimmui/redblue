from django.contrib import admin

from .models import ColorTeam, Voter

@admin.register(Voter)
class clipCategoryAdmin(admin.ModelAdmin):
    list_display = ['email', 'choice']

@admin.register(ColorTeam)
class clipColorTeam(admin.ModelAdmin):
    list_display = ['name', 'votes']