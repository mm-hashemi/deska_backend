from rest_framework import viewsets, permissions
from django.db.models import Q
from .models import Board
from .serializers import BoardSerializer

class BoardViewSet(viewsets.ModelViewSet):
    """
    این viewset فقط بردهایی را به کاربر نشان می‌دهد که مالک، عضو
    یا عضو تیم آن است، یا تیمی که خودش owner آن است.
    """
    serializer_class = BoardSerializer
    permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        # هنگام ساخت برد جدید، owner را کاربر فعلی قرار بده
        serializer.save(owner=self.request.user)

    def get_queryset(self):
        user = self.request.user
        # فقط بردهایی را نمایش بده که کاربر متعلق به آنهاست یا آنها را ساخته
        return Board.objects.filter(
            Q(owner=user) |
            Q(members=user) |
            Q(team__members=user) |
            Q(team__owner=user)
        ).distinct()
        
    def get_serializer_context(self):
        """
        اگر در serializer به request نیاز داری، اینجا به context اضافه کن
        """
        context = super().get_serializer_context()
        context['request'] = self.request
        return context
