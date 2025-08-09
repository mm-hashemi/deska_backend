from rest_framework import serializers
from .models import Board
from accounts.models import User
from accounts.serializers import UserSerializer
from teams.serializers import TeamDetailSerializer  # یا TeamListSerializer بسته به نیاز
from teams.models import Team

class BoardSerializer(serializers.ModelSerializer):
    owner = UserSerializer(read_only=True)
    members = UserSerializer(many=True, read_only=True)
    team = TeamDetailSerializer(read_only=True)  # نمایش اطلاعات کامل تیم
    team_id = serializers.PrimaryKeyRelatedField(
        queryset=Team.objects.all(), source='team', write_only=True, required=False, allow_null=True
    )

    class Meta:
        model = Board
        fields = [
            'id', 'name', 'team', 'team_id', 'description', 'owner', 'members',
            'color', 'status', 'created_at', 'updated_at'
        ]
        read_only_fields = ['owner', 'members', 'team', 'created_at', 'updated_at', 'id']

    def create(self, validated_data):
        user = self.context['request'].user

        if 'owner' in validated_data:
           validated_data.pop('owner')

    # ساخت برد
        board = Board.objects.create(owner=user, **validated_data)
        board.members.set([user])
        return board

     