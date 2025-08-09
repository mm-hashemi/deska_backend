from rest_framework import viewsets, permissions, status
from rest_framework.decorators import action
from rest_framework.response import Response
from django.shortcuts import get_object_or_404
from django.db.models import Count
from boards.models import Team, Board
from .serializers import (
    TeamListSerializer,
    TeamDetailSerializer,
    TeamCreateSerializer,
    ProjectSerializer
)

class IsOwnerOrReadOnly(permissions.BasePermission):
    def has_object_permission(self, request, view, obj):
        if request.method in permissions.SAFE_METHODS:
            return True
        return obj.owner == request.user


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()  # اضافه‌شد تا DRF basename رو پیدا کنه
    permission_classes = [permissions.IsAuthenticatedOrReadOnly, IsOwnerOrReadOnly]

    def get_queryset(self):
        user = self.request.user
        base_qs = Team.objects.all().prefetch_related('members', 'boards').select_related('owner')
        if user.is_authenticated:
            return base_qs.filter(members=user).annotate(projects_count=Count('boards'))
        return base_qs.annotate(projects_count=Count('boards'))

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        elif self.action == 'retrieve':
            return TeamDetailSerializer
        elif self.action == 'create':
            return TeamCreateSerializer
        return TeamDetailSerializer

    def perform_create(self, serializer):
        serializer.save(owner=self.request.user)

    @action(detail=True, methods=['get'], permission_classes=[permissions.IsAuthenticatedOrReadOnly])
    def projects(self, request, pk=None):
        """
        GET /api/teams/{pk}/projects/  -> لیست پروژه‌های این تیم
        """
        team = get_object_or_404(Team, pk=pk)

        # اطمینان از اینکه فقط اعضای تیم می‌توانند لیست پروژه‌ها را ببینند
        if request.user not in team.members.all() and request.user != team.owner:
            return Response({'detail': 'You do not have permission to view projects of this team.'},
                            status=status.HTTP_403_FORBIDDEN)

        projects_qs = team.projects.all()
        page = self.paginate_queryset(projects_qs)
        serializer = ProjectSerializer(page or projects_qs, many=True, context={'request': request})
        if page is not None:
            return self.get_paginated_response(serializer.data)
        return Response(serializer.data)
