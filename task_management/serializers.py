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
    class Meta:
        model = Task
        fields = ['client', 'worker', 'required_skill', 'title', 'description', 'start_time', 'end_time', 'location', 'remuneration', 'is_finished']
        read_only_fields = ['client', 'worker', 'start_time', 'end_time', 'is_finished']
    
    def __init__(self, *args, **kwargs):
        super(TaskSerializer, self).__init__(*args, **kwargs)
        if 'request' in self.context:
            if self.context['request'].method in ['POST']:
                self.fields['client'].required = False
                self.fields['worker'].required = False
                self.fields['start_time'].required = False
                self.fields['end_time'].required = False
                self.fields['is_finished'].required = False
