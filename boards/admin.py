from django.contrib import admin
from .models import Board

@admin.register(Board)
class BoardAdmin(admin.ModelAdmin):
    list_display = ('name', 'owner', 'status', 'color', 'created_at')
    search_fields = ('name', 'description', 'owner__email')
    list_filter = ('status', 'color', 'created_at')
    filter_horizontal = ('members',)
