import redis
from geopy.distance import geodesic
from geopy.geocoders import Nominatim
from .models import Task, UserProfile
import time
import json

# 初始化 Redis 客戶端
r = redis.StrictRedis(host='redis', port=6379, db=0)  # 使用 Docker Compose 服務名作為主機名

def get_cached_coordinates(address):
    # 從 Redis 中查詢經緯度
    cached_location = r.get(f"location:{address}")
    if cached_location:
        return json.loads(cached_location)
    else:
        # 如果 Redis 中沒有，則使用 Nominatim 查詢
        return get_coordinates(address)

def get_coordinates(address):
    geolocator = Nominatim(user_agent="task_allocation_system")
    location = geolocator.geocode(address)
    if location:
        # 將經緯度結果保存到 Redis 中，有效期 1 天（86400 秒）
        r.setex(f"location:{address}", 86400, json.dumps((location.latitude, location.longitude)))
        return (location.latitude, location.longitude)
    else:
        return None

def find_worker(task):
    task_location = get_cached_coordinates(task.location)
    if not task_location:
        print("Task location could not be converted to coordinates.")
        return

    while True:
        # 獲取可用工人的位置信息
        available_workers = UserProfile.objects.filter(is_working=True, on_duty=False)

        # 根據技能匹配工人
        matched_workers = [worker for worker in available_workers if worker.has_skills(task.skill)]

        nearby_workers = []
        for worker in matched_workers:
            # 每30秒更新工人的經緯度
            worker_location = get_worker_location(worker)  # 假設這是一個獲取工人位置的函數
            if worker_location:
                distance = geodesic(task_location, worker_location).km
                if distance <= 3:
                    nearby_workers.append((worker, distance))

        if nearby_workers:
            closest_worker, closest_distance = min(nearby_workers, key=lambda w: w[1])
            closest_worker.on_duty = True
            closest_worker.save()
            task.worker = closest_worker
            task.save()

            print(f"Worker {closest_worker} (distance: {closest_distance:.2f} km) assigned to task {task}")
            break
        else:
            print("No available workers within 3 km, retrying in 30 seconds...")
            time.sleep(30)  # 等待30秒後重新查詢

def get_worker_location(worker):
    # 獲取工人的最新位置
    location = r.get(f"worker_location:{worker.id}")
    if location:
        return json.loads(location)  # 返回工人的經緯度
    return None  # 如果沒有找到位置，返回None
