import redis
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from .models import Task, UserProfile, UserSkill
import time
import json

# 初始化 Redis 客戶端
# r = redis.StrictRedis(host='redis', port=6379, db=0)  # 使用 Docker Compose 服務名作為主機名

# def get_cached_coordinates(location):
#     # 從 Redis 中查詢經緯度
#     cached_location = r.get(f"location:{location}")
#     if cached_location:
#         return json.loads(cached_location)
#     else:
#         # 如果 Redis 中沒有，則使用 Nominatim 查詢
#         return get_coordinates(location)

def get_coordinates(location):
    geolocator = Nominatim(user_agent="task_allocation_system")
    location = geolocator.geocode(location)
    if location:
        # 將經緯度結果保存到 Redis 中，有效期 1 天（86400 秒）
        # r.setex(f"location:{location}", 86400, json.dumps((location.latitude, location.longitude)))
        print('location is:', location.latitude, location.longitude)
        return (location.latitude, location.longitude)
    else:
        return None

def find_worker(required_skill, location):
    # task_location = get_cached_coordinates(location)
    task_location = get_coordinates(location)
    if not task_location:
        print("Task location could not be converted to coordinates.")
        return
    count = 0
    while True:
        # 根據技能匹配工人
        available_workers = UserProfile.objects.filter(
            on_duty=True, 
            is_working=False,
            id__in=UserSkill.objects.filter(skill=required_skill).values_list('user_profile_id', flat=True),
        ).distinct()
        print(available_workers)

        nearby_workers = []
        for worker in available_workers:
            # 每30秒更新工人的經緯度
            worker_location = get_coordinates(worker.user_location)  # 假設這是一個獲取工人位置的函數
            if worker_location:
                distance = geodesic(task_location, worker_location).km
                if distance <= 10:
                    nearby_workers.append((worker, distance))

        if nearby_workers:
            closest_worker, closest_distance = min(nearby_workers, key=lambda w: w[1])
            # closest_worker.on_duty = True
            # closest_worker.save()
            # task.worker = closest_worker
            # task.save()

            # print(f"Worker {closest_worker} (distance: {closest_distance:.2f} km) assigned to task {task}")
            # break

            return closest_worker

        if count >= 5:
            print("No available workers")
            return(None)
        else:
            count += 1
            print("No available workers within 3 km, retrying in 3 seconds...")
            time.sleep(3)  # 等待3秒後重新查詢

def find_worker_by_skill(required_skill):
    count = 0
    while True:
        # 根據技能查詢符合要求的工人，並且檢查他們是否正在執勤且未被分配任務
        skill_matched_worker_profiles = UserProfile.objects.filter(
            on_duty=True, 
            is_working=False,
            id__in=UserSkill.objects.filter(skill=required_skill).values_list('user_profile_id', flat=True),
        ).distinct()

        print(skill_matched_worker_profiles)

        if skill_matched_worker_profiles.exists():
            # 返回第一個符合要求的工人
            return skill_matched_worker_profiles.first()
        if count >= 5:
            print("No available workers")
            return(None)
        else:
            count += 1
            print("No available workers, retrying in 3 seconds...")
            time.sleep(3)  # 等待3秒後重新查詢

        # skill_matched_worker = UserSkill.objects.filter(skills=required_skill)
        # available_workers = UserProfile.objects.filter(is_working=False, on_duty=True)
        # print(UserProfile.objects)
        # # 根據技能匹配工人
        # matched_workers = [worker for worker in available_workers if worker.skills(required_skill)]
    
        # if count >= 5:
        #     print("No available workers")
        #     break
        # elif matched_workers:
        #     return matched_workers[0]
        # else:
        #     count += 1
        #     print("No available workers within 3 km, retrying in 3 seconds...")
        #     time.sleep(3)  # 等待3秒後重新查詢


# def get_worker_location(worker):
#     # 獲取工人的最新位置
#     location = r.get(f"worker_location:{worker.id}")
#     if location:
#         return json.loads(location)  # 返回工人的經緯度
#     return None  # 如果沒有找到位置，返回None
