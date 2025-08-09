# apps/teams/serializers.py
from rest_framework import serializers
from boards.models import Team, Board
from django.contrib.auth import get_user_model

User = get_user_model()

class SimpleUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'first_name', 'last_name', 'email')

class ProjectSerializer(serializers.ModelSerializer):
    class Meta:
        model = Board
        fields = ('id', 'name', 'description', 'owner', 'created_at')

class TeamListSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)
    members = SimpleUserSerializer(many=True, read_only=True)
    boards_count = serializers.IntegerField(source='boards.count', read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'owner', 'members', 'boards_count', 'created_at')

class TeamDetailSerializer(serializers.ModelSerializer):
    owner = SimpleUserSerializer(read_only=True)
    members = SimpleUserSerializer(many=True, read_only=True)
    projects = ProjectSerializer(many=True, read_only=True)
    boards_count = serializers.IntegerField(source='boards.count', read_only=True)

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'owner', 'members', 'boards_count','projects', 'boards', 'created_at')

class TeamCreateSerializer(serializers.ModelSerializer):
    # گرفتن لیست member IDs
    members = serializers.ListField(
        child=serializers.IntegerField(),
        write_only=True,
        required=False
    )

    class Meta:
        model = Team
        fields = ('id', 'name', 'description', 'members')

    def create(self, validated_data):
        user = self.context['request'].user

        # جدا کردن شناسه کاربران قبل از ساخت تیم
        member_ids = validated_data.pop('members', [])

        # حذف owner اگر به هر دلیل همراه داده‌ها آمده بود
        validated_data.pop('owner', None)

        # ساخت تیم با owner فعلی
        team = Team.objects.create(owner=user, **validated_data)

        # اضافه کردن اعضا
        if member_ids:
            users = User.objects.filter(id__in=member_ids)
            team.members.set(users)
        # همیشه owner هم عضو تیم باشه
        team.members.add(user)

        return team