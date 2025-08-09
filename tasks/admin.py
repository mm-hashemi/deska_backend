from django.contrib import admin
from .models import Task, Tag, Sprint, Attachment

@admin.register(Task)
class TaskAdmin(admin.ModelAdmin):
    list_display = ('title', 'board', 'assigned_to', 'status', 'priority', 'created_at')
    search_fields = ('title', 'description')
    list_filter = ('status', 'color', 'priority', 'board', 'sprint')
    filter_horizontal = ('tags', 'dependencies',)

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'color')
    search_fields = ('name',)

@admin.register(Sprint)
class SprintAdmin(admin.ModelAdmin):
    list_display = ('name', 'board', 'start_date', 'end_date', 'is_active')
    list_filter = ('board', 'is_active')

@admin.register(Attachment)
class AttachmentAdmin(admin.ModelAdmin):
    list_display = ('id', 'task', 'file', 'uploaded_by', 'uploaded_at')
    search_fields = ('task__title', 'file')
