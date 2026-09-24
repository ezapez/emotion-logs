from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone


class Entry(models.Model):
    EMOTION_CHOICES = [
        ('Happy', 'Happy'),
        ('Sad', 'Sad'),
        ('Angry', 'Angry'),
        ('Anxious', 'Anxious'),
        ('Calm', 'Calm'),
        ('Excited', 'Excited'),
        ('Other', 'Other'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE)
    date = models.DateField(default=timezone.localdate)
    emotion = models.CharField(max_length=20, choices=EMOTION_CHOICES)
    experience = models.TextField()
    date_added = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date', '-date_added']
        verbose_name_plural = 'entries'

    def __str__(self):
        return f"{self.date}: {self.emotion}"
    


