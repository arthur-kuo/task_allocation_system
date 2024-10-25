from rest_framework import viewsets, status, decorators
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from .models import UserProfile, Skill, UserSkill, Task
from .serializers import UserProfileSerializer, SkillSerializer, UserSkillSerializer, TaskSerializer
from .services import find_worker, find_worker_by_skill
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import action
from datetime import datetime
# from rest_framework.permissions import AllowAny

class UserProfileViewSet(viewsets.ModelViewSet):
    queryset = UserProfile.objects.all()
    serializer_class = UserProfileSerializer

class SkillViewSet(viewsets.ModelViewSet):
    queryset = Skill.objects.all()
    serializer_class = SkillSerializer

class UserSkillViewSet(viewsets.ModelViewSet):
    queryset = UserSkill.objects.all()
    serializer_class = UserSkillSerializer

class TaskViewSet(viewsets.ModelViewSet):
    queryset = Task.objects.all()
    serializer_class = TaskSerializer
    # authentication_classes = []  # 禁用身份验证
    # permission_classes = [AllowAny]  # 允许任何人访问
    # permission_class = [IsAuthenticated]
    # 透過驗證可得知client 資訊

    def get_tasks(self):
        user_profile = self.request.user.userprofile 
        print(Task.objects.filter(client=user_profile))
        return Task.objects.filter(client=user_profile)

    def get_task(self, request):
        task_id = kwargs.get('id')
        task = self.get_object()
        if task.client != request.user.userprofil:
            return Response({'detail': 'You do not have permission to view this task.'}, status=status.HTTP_403_FORBIDDEN)
        return super().retrieve(request, *args, **kwargs)

    def create(self, request):
        serializer = TaskSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        # 獲取 client 和必要的輸入資訊
        client = self.request.user.userprofile # 從 request 中自動取得 client

        # return Response({'client': client})
        required_skill = serializer.validated_data.get('required_skill')
        location = serializer.validated_data.get('location')
        print('task location is:', location)
        print("client is:", client.user.username)
        print("client location:", client.user_location)
        print("client on duty status:", client.on_duty)
        print("client is working:", client.is_working)

        # 查找 worker
        worker = find_worker(required_skill, location)
        # worker = find_worker_by_skill(required_skill)
        if not worker:
            return Response({'detail': 'No available worker found'}, status=status.HTTP_400_BAD_REQUEST)

        print('worker is:' , worker.user.username)
        print("worker location:", worker.user_location)
        print("worker on duty status:", worker.on_duty)
        print("worker is working:", worker.is_working)

        # 保存 Task 並自動設置 client 和 worker
        worker.is_working = True
        worker.save()
        print("worker is working:", worker.is_working)
        task = serializer.save(client=client, worker=worker)
        full_task_serializer = TaskSerializer(task)

        # 使用完整的 serializer 返回任務資料
        return Response(full_task_serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, id = None):
        task = self.get_object()
        if task.client != request.user:
            return Response({'detail': 'You do not have permission to cancel this task.'}, status=status.HTTP_403_FORBIDDEN)
        elif task.is_finished:
            return Response({'detail': "Can't cancel a finished task."}, status=status.HTTP_400_BAD_REQUEST) # 已完成的任務不能取消(刪除)
        task.delete()
        return Response({'detail': 'Task canceled.'}, status=status.HTTP_200_OK) 

    def update(self, request, *args, **kwargs):
        return Response({'detail': 'Update operation is not allowed.'}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    def partial_update(self, request, pk=None):
        serializer = TaskSerializer(data=self.request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)
        # 只更新 end_time 和 is_finished
        task = self.get_object()
        task.end_time = serializer.validated_data.get('end_time', datetime.now().isoformat(timespec='seconds') + '+08:00')
        task.is_finished = serializer.validated_data.get('is_finished', True)
        task.save()
        return Response(TaskSerializer(task).data, status=status.HTTP_200_OK)

