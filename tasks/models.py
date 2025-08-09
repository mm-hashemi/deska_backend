from django.db import models
from boards.models import Board
from django.conf import settings

class Sprint(models.Model):
    board = models.ForeignKey(Board, related_name="sprints", on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    start_date = models.DateField()
    end_date = models.DateField()
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.board.name} - {self.name}"

class Tag(models.Model):
    name = models.CharField(max_length=50)
    color = models.CharField(max_length=8, default="#1976d2")  # برچسب آبی پیش‌فرض

    def __str__(self):
        return self.name

class Group(models.Model):
    title = models.CharField(max_length=100)
    board = models.ForeignKey(Board, on_delete=models.CASCADE, related_name='groups')
    order = models.PositiveIntegerField(default=0)
    color = models.CharField(max_length=16, blank=True, null=True)
    deadline = models.DateField(blank=True, null=True)  # این خط اضافه شد

    def __str__(self):
        return self.title

class Task(models.Model):
    COLOR_CHOICES = [
        ('#1976d2', 'آبی'),
        ('#43a047', 'سبز'),
        ('#ffb300', 'زرد'),
        ('#d32f2f', 'قرمز'),
        ('#7b1fa2', 'بنفش'),
        ('#455a64', 'خاکستری'),
    ]
    STATUS_CHOICES = (
        ('todo', 'To Do'),
        ('in_progress', 'In Progress'),
        ('done', 'Done'),
    )

    title = models.CharField(max_length=255)
    description = models.TextField(blank=True)
    board = models.ForeignKey(Board, related_name="tasks", on_delete=models.CASCADE)

    assigned_to = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='assigned_tasks',
        null=True, blank=True, on_delete=models.SET_NULL,
        help_text="کاربر مسئول این تسک"
    )

    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default='todo'
    )

    color = models.CharField(
        max_length=8, choices=COLOR_CHOICES, default='#1976d2',
        help_text="رنگ نمایشی این تسک"
    )
    completed_at = models.DateTimeField(null=True, blank=True)
    start_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)

    sprint = models.ForeignKey(
        Sprint, related_name="tasks", null=True, blank=True, on_delete=models.SET_NULL
    )

    tags = models.ManyToManyField(Tag, related_name='tasks', blank=True)
    dependencies = models.ManyToManyField('self', symmetrical=False, blank=True, related_name='dependents')

    group = models.ForeignKey(
        Group, related_name='tasks', null=True, blank=True, on_delete=models.SET_NULL,
        help_text="ستون برد یا گروه"
    )

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    priority = models.PositiveSmallIntegerField(
        default=1, help_text="۱: معمولی، ۲: مهم، ۳: خیلی مهم"
    )
    progress = models.PositiveSmallIntegerField(default=0, help_text="درصد انجام (۰ تا ۱۰۰)")

    def __str__(self):
        return f"{self.title} ({self.board.name})"

class Attachment(models.Model):
    task = models.ForeignKey(Task, related_name='attachments', on_delete=models.CASCADE)
    file = models.FileField(upload_to='attachments/', blank=True, null=True)
    uploaded_at = models.DateTimeField(auto_now_add=True)
    uploaded_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, related_name='uploaded_attachments', on_delete=models.CASCADE,
        null=True, blank=True
    )

    def __str__(self):
        if self.file and self.file.name:
            file_name = self.file.name
        else:
            file_name = "بدون فایل"
        return f"{self.task.title} - {file_name}"
