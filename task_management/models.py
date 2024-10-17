from django.db import models
from django.contrib.auth.models import User

class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    user_location = models.CharField(max_length=255)
    on_duty = models.BooleanField(default=False)
    is_working = models.BooleanField(default=False)

class Skill(models.Model):
    skill_name = models.CharField(max_length=255)

class UserSkill(models.Model):
    user_profile = models.ForeignKey(UserProfile, on_delete=models.CASCADE)
    skill = models.ForeignKey(Skill, on_delete=models.CASCADE)

class Task(models.Model):
    client = models.ForeignKey(UserProfile, related_name='client_tasks', on_delete=models.CASCADE)
    worker = models.ForeignKey(UserProfile, related_name='worker_tasks', null=True, blank=True, on_delete=models.CASCADE)
    required_skill = models.ForeignKey(Skill,  null=True, blank=True, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
    location = models.CharField(max_length=255)
    remuneration = models.IntegerField(null=True, blank=True)
    task_location = models.CharField(max_length=255, default='Unknown')
    is_finished = models.BooleanField(default=False)

