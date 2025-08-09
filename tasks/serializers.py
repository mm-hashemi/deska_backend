from rest_framework import serializers
from .models import Sprint, Tag, Task, Attachment, Board,Group
from django.contrib.auth import get_user_model

User = get_user_model()

class TaskSerializer(serializers.ModelSerializer):
    class Meta:
        model = Task
        fields = [
            'id', 'title', 'description', 'due_date', 'board', 'sprint', 'tags',
            'assigned_to', 'status', 'color', 'dependencies', 'priority',
            'created_at', 'updated_at'
        ]
class UserSimpleSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'first_name','avatar']

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tag
        fields = ['id', 'name']

class SprintSerializer(serializers.ModelSerializer):
    class Meta:
        model = Sprint
        fields = ['id', 'name', 'board', 'start_date', 'end_date']

class AttachmentSerializer(serializers.ModelSerializer):
    uploaded_by = serializers.StringRelatedField(read_only=True)
    class Meta:
        model = Attachment
        fields = ['id', 'file', 'uploaded_at', 'uploaded_by']


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'title', 'board', 'order', 'color']
