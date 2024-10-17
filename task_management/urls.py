from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import UserProfileViewSet, SkillViewSet, UserSkillViewSet, TaskViewSet

router = DefaultRouter()
router.register(r'userprofiles', UserProfileViewSet)
router.register(r'skills', SkillViewSet)
router.register(r'userskills', UserSkillViewSet)
router.register(r'tasks', TaskViewSet)

urlpatterns = [
    path('', include(router.urls)),
]