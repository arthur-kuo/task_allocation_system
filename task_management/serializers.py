from rest_framework import serializers
from django.contrib.auth.models import User
from .models import UserProfile, Skill, UserSkill, Task

class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'email']

class UserProfileSerializer(serializers.ModelSerializer):
    user = UserSerializer()

    class Meta:
        model = UserProfile
        fields = ['user', 'user_location', 'on_duty', 'is_working']

class SkillSerializer(serializers.ModelSerializer):
    class Meta:
        model = Skill
        fields = ['id', 'skill_name']

class UserSkillSerializer(serializers.ModelSerializer):
    user_profile = UserProfileSerializer()
    skill = SkillSerializer()

    class Meta:
        model = UserSkill
        fields = ['user_profile', 'skill']

class TaskSerializer(serializers.ModelSerializer):
    client = UserProfileSerializer()
    worker = UserProfileSerializer()

    class Meta:
        model = Task
        fields = ['id', 'client', 'worker', 'title', 'description', 'start_time', 'end_time', 'location', 'remuneration', 'task_location', 'is_finished']