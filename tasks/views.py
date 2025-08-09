from rest_framework import viewsets, permissions
from .models import Task, Sprint, Tag, Group  # ← مدل های جدید
from .serializers import (TaskSerializer, UserSimpleSerializer, SprintSerializer, TagSerializer, GroupSerializer)
from django.contrib.auth import get_user_model

User = get_user_model()

class UserViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSimpleSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        queryset = super().get_queryset()
        board_id = self.request.query_params.get('board')
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset

    def perform_create(self, serializer):
        # اگر board ForeignKey است و مقدار id را میفرستی (عدد)، همین کافیست
        serializer.save(board_id=self.request.data.get('board', None))

class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        board_id = self.request.query_params.get("board")
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset

    def get_queryset(self):
        queryset = super().get_queryset()
        board_id = self.request.query_params.get('board')
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset

class SprintViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Sprint.objects.all()
    serializer_class = SprintSerializer

    def get_queryset(self):
        queryset = super().get_queryset()
        board_id = self.request.query_params.get('board')
        if board_id:
            queryset = queryset.filter(board_id=board_id)
        return queryset

class TagViewSet(viewsets.ModelViewSet):  # اگر می‌خواهی CRUD کامل  
    queryset = Tag.objects.all()
    serializer_class = TagSerializer
