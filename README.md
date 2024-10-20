# 即時任務分配系統

此系統使用 Django 開發，能夠根據臨時任務的技能需求和地理位置自動分配合適的工人。系統透過 WebSocket 實時更新工人的位置，並使用 Redis 快取位置數據。

## 功能特色
1. **使用者認證**：支援基於 JWT 的使用者註冊與登入功能。
2. **任務管理**：客戶可以創建、更新、刪除臨時任務。每個任務包括標題、描述、開始時間、結束時間、地點、技能需求與報酬金額等資訊。
3. **任務分配**：系統會自動根據地理位置、技能和可用時間等條件，匹配最適合的工人。若無符合條件的工人在 3 公里內，系統每 30 秒重新查詢一次。
4. **即時更新**：通過 WebSocket，每 30 秒將選定工人的位置更新給客戶，直到任務結束。
5. **Redis 快取**：使用 Redis 快取地址的經緯度數據，提升查詢效能。

## 系統架構
1. **資料庫**：系統使用 MySQL 或 PostgreSQL 存儲用戶、任務和工人的相關資訊。
2. **WebSocket 實時更新**：系統透過 WebSocket 實時傳輸工人的位置信息，讓客戶能夠即時查看工人的行進路線。
3. **任務結束處理**：任務完成後，工人和客戶都可以確認任務已結束，並更新任務狀態。WebSocket 連線會在任務完成後斷開。

## 資料庫結構 (ERD)
![資料庫結構](https://github.com/arthur-kuo/task_allocation_system/blob/main/images/ERD.jpg)

## 安裝與使用
1. clone此專案：
   ```bash
   git clone https://github.com/arthur-kuo/task_allocation_system.git
   ```
2. 進入專案資料夾並安裝相依套件：
   ```bash
   cd task_allocation_system
   pip install -r requirements.txt
   ```
3. 設定環境變數 `.env` 文件：
   ```
   DB_NAME=your_database_name
   DB_USER=your_database_user
   DB_PASSWORD=your_database_password
   DB_ROOT_PASSWORD=your_database_root_password
   DB_HOST=your_database_host
   DB_PORT=your_database_port
   REDIS_HOST=your_redis_host
   REDIS_PORT=your_redis_port
   ```
4. 遷移資料庫：
   ```bash
   python manage.py migrate
   ```
5. 啟動服務：
   ```bash
   docker-compose up
   ```

## API文件

1. 以Swagger生成, 路徑為 /api/docs/

2. [API文檔](https://github.com/arthur-kuo/task_allocation_system/blob/main/docs/API.md)

## 使用技術
- **後端框架**：Django, Django REST Framework
- **即時更新**：WebSocket
- **資料庫**：MySQL / PostgreSQL
- **快取**：Redis
- **容器**：Docker, Docker Compose

## 開發者
- [Arthur Kuo](https://github.com/arthur-kuo)
