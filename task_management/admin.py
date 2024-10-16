from django.contrib import admin
from .models import UserProfile, Task, Skill, UserSkill

admin.site.register(UserProfile)
admin.site.register(Task)
admin.site.register(Skill)
admin.site.register(UserSkill)
