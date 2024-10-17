# API 文件

此 API 提供用戶創建、讀取、更新和刪除任務，管理用戶及個人資料，並實時分配任務給適合的工作者。

## 認證
此 API 使用 JWT 進行身份驗證，所有受保護的請求必須在請求頭的 Authorization 中包含有效的 JWT 令牌。

### API 端點

---

### **1. 註冊新用戶**

**URL**: `/api/auth/register/`  
**方法**: `POST`  
**描述**: 註冊新用戶，包含用戶名、電子郵件和密碼。

**請求**:
```json
{
  "username": "example_user",
  "email": "user@example.com",
  "password": "example_password",
  "password2": "example_password"
}
```

**回應**:
- `201 Created`
```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com"
}
```

**錯誤回應**:
- `400 Bad Request` - 密碼不一致，或該電子郵件已經存在。

---

### **2. 登入**

**URL**: `/api/auth/login/`  
**方法**: `POST`  
**描述**: 用戶登錄並返回 JWT 令牌。

**請求**:
```json
{
  "username": "example_user",
  "password": "example_password"
}
```

**回應**:
- `200 OK`
```json
{
  "token": "your_jwt_token"
}
```

---

### **3. 創建任務**

**URL**: `/api/tasks/`  
**方法**: `POST`  
**描述**: 創建新任務，並指定客戶和工作者。

**請求**:
```json
{
  "client": {
    "user": {
      "id": 1,
      "username": "client_user",
      "email": "client@example.com"
    },
    "user_location": "Taipei",
    "on_duty": true,
    "is_working": false
  },
  "worker": {
    "user": {
      "id": 2,
      "username": "worker_user",
      "email": "worker@example.com"
    },
    "user_location": "New Taipei",
    "on_duty": true,
    "is_working": true
  },
  "title": "Deliver a package",
  "description": "Deliver a package from Taipei to New Taipei",
  "start_time": "2024-10-17T10:00:00Z",
  "end_time": "2024-10-17T12:00:00Z",
  "location": "Taipei",
  "remuneration": 500,
  "task_location": "New Taipei",
  "is_finished": false
}
```

**回應**:
- `201 Created`
```json
{
  "id": 1,
  "client": {
    "user": {
      "id": 1,
      "username": "client_user",
      "email": "client@example.com"
    },
    "user_location": "Taipei",
    "on_duty": true,
    "is_working": false
  },
  "worker": {
    "user": {
      "id": 2,
      "username": "worker_user",
      "email": "worker@example.com"
    },
    "user_location": "New Taipei",
    "on_duty": true,
    "is_working": true
  },
  "title": "Deliver a package",
  "description": "Deliver a package from Taipei to New Taipei",
  "start_time": "2024-10-17T10:00:00Z",
  "end_time": "2024-10-17T12:00:00Z",
  "location": "Taipei",
  "remuneration": 500,
  "task_location": "New Taipei",
  "is_finished": false
}
```

---

### **4. 查詢任務**

**URL**: `/api/tasks/{id}/`  
**方法**: `GET`  
**描述**: 根據 ID 查詢特定任務。

**回應**:
- `200 OK`
```json
{
  "id": 1,
  "client": {
    "user": {
      "id": 1,
      "username": "client_user",
      "email": "client@example.com"
    },
    "user_location": "Taipei",
    "on_duty": true,
    "is_working": false
  },
  "worker": {
    "user": {
      "id": 2,
      "username": "worker_user",
      "email": "worker@example.com"
    },
    "user_location": "New Taipei",
    "on_duty": true,
    "is_working": true
  },
  "title": "Deliver a package",
  "description": "Deliver a package from Taipei to New Taipei",
  "start_time": "2024-10-17T10:00:00Z",
  "end_time": "2024-10-17T12:00:00Z",
  "location": "Taipei",
  "remuneration": 500,
  "task_location": "New Taipei",
  "is_finished": false
}
```

---

### **5. 更新任務**

**URL**: `/api/tasks/{id}/`  
**方法**: `PUT`  
**描述**: 更新特定任務的細節。

**請求**:
```json
{
  "title": "New Task Title",
  "description": "Updated description"
}
```

**回應**:
- `200 OK`
```json
{
  "id": 1,
  "title": "New Task Title",
  "description": "Updated description"
}
```

---

### **6. 刪除任務**

**URL**: `/api/tasks/{id}/`  
**方法**: `DELETE`  
**描述**: 刪除特定任務。

**回應**:
- `204 No Content`  

---

### **7. 查詢用戶**

**URL**: `/api/users/{id}/`  
**方法**: `GET`  
**描述**: 根據 ID 查詢用戶資訊。

**回應**:
- `200 OK`
```json
{
  "id": 1,
  "username": "example_user",
  "email": "user@example.com"
}
```