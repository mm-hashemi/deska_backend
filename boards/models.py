from django.db import models
from django.conf import settings
from teams.models import Team

class Board(models.Model):
    COLOR_CHOICES = [
        ("#1976d2", 'blue'),
        ("#6ce272", 'green'),
        ("#ffd36c", 'yellow'),
        ("#ff7272", 'red'),
        ("#d681fb", 'purple'),
        ("#627b87", 'gray'),
    ]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('archived', 'Archived'),
        ('closed', 'Closed'),
    ]

    name = models.CharField(
        max_length=255,
        verbose_name="Project Name",
        help_text="Name of the project or board"
    )
    team = models.ForeignKey(
        Team,
        on_delete=models.CASCADE,
        related_name='boards',
        null=True, blank=True,
        help_text="Team this board belongs to (can be empty)"
    )
    description = models.TextField(
        blank=True,
        help_text="Board description (optional)"
    )
    color = models.CharField(
        max_length=16,
        choices=COLOR_CHOICES,
        default='#1976d2',
        help_text="Board color (default: blue)"
    )
    status = models.CharField(
        max_length=16,
        choices=STATUS_CHOICES,
        default='active',
        help_text="Status of the board"
    )
    owner = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        related_name='owned_boards',
        on_delete=models.CASCADE,
        help_text="User who created/owns the board"
    )
    members = models.ManyToManyField(
        settings.AUTH_USER_MODEL,
        related_name='boards',
        blank=True,
        help_text="Board team members"
    )
    created_at = models.DateTimeField(
        auto_now_add=True, editable=False
    )
    updated_at = models.DateTimeField(
        auto_now=True
    )

    class Meta:
        ordering = ['-created_at']
        verbose_name = "Board"
        verbose_name_plural = "Boards"

    def __str__(self):
        return self.name
