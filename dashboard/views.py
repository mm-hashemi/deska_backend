from datetime import date, timedelta
from django.db.models import Count
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from tasks.models import Task

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def overview(request):
    user = request.user

    # شروع هفته (دوشنبه به عنوان اولین روز هفته)
    week_start = date.today() - timedelta(days=date.today().weekday())

    # شمارش کلی
    active_tasks = Task.objects.filter(
        assigned_to=user,
        status__in=['todo', 'in_progress']
    ).count()

    projects_count = user.teams.values('boards').distinct().count()

    completed_this_week = Task.objects.filter(
        assigned_to=user,
        status='done',
        updated_at__gte=week_start
    ).count()

    # دیتای چارت
    labels = []
    completed_tasks_data = []
    new_issues_data = []

    for i in range(7):
        day = week_start + timedelta(days=i)
        next_day = day + timedelta(days=1)

        labels.append(day.strftime("%a"))  # Mon, Tue, ...

        completed_count = Task.objects.filter(
            assigned_to=user,
            status='done',
            updated_at__gte=day,
            updated_at__lt=next_day
        ).count()

        new_issues_count = Task.objects.filter(
            assigned_to=user,
            created_at__gte=day,
            created_at__lt=next_day
        ).count()

        completed_tasks_data.append(completed_count)
        new_issues_data.append(new_issues_count)

    return Response({
        "active_tasks": active_tasks,
        "projects": projects_count,
        "completed_this_week": completed_this_week,
        "chart": {
            "labels": labels,
            "completed_tasks": completed_tasks_data,
            "new_issues": new_issues_data
        }
    })
