"""
集中存储所有模拟数据，供路由使用
"""
from datetime import datetime, timedelta

# 用户模拟数据
MOCK_USERS = {
    "user@example.com": {
        "id": "1",
        "name": "张三",
        "email": "user@example.com",
        "password": "password123",
        "role": "user",
        "status": "active"
    },
    "admin@example.com": {
        "id": "2",
        "name": "管理员",
        "email": "admin@example.com",
        "password": "admin123",
        "role": "admin",
        "status": "active"
    }
}

# 用户列表格式（用于API响应）
MOCK_USERS_LIST = [
    {
        "id": "1",
        "name": "张三",
        "email": "user@example.com",
        "role": "user",
        "status": "active",
        "createdAt": "2023-01-01T08:00:00Z",
        "updatedAt": "2023-01-01T08:00:00Z",
        "lastLoginAt": "2023-10-15T14:30:00Z"
    },
    {
        "id": "2",
        "name": "管理员",
        "email": "admin@example.com",
        "role": "admin",
        "status": "active",
        "createdAt": "2023-01-01T08:00:00Z",
        "updatedAt": "2023-01-01T08:00:00Z",
        "lastLoginAt": "2023-11-01T09:15:00Z"
    },
    {
        "id": "3",
        "name": "李四",
        "email": "lisi@example.com",
        "role": "user",
        "status": "inactive",
        "createdAt": "2023-02-01T08:00:00Z",
        "updatedAt": "2023-02-01T08:00:00Z",
        "lastLoginAt": "2023-05-20T16:45:00Z"
    }
]

# 预约模拟数据
MOCK_RESERVATIONS = [
    {
        "id": "1",
        "seatId": "101",
        "seatNumber": "A1",
        "location": "图书馆一楼",
        "userId": "1",
        "date": "2023-11-10",
        "timeSlot": "09:00-10:00",
        "status": "已预约",
        "createdAt": datetime.now() - timedelta(days=2),
        "updatedAt": datetime.now() - timedelta(days=2),
    },
    {
        "id": "2",
        "seatId": "102",
        "seatNumber": "B2",
        "location": "图书馆二楼",
        "userId": "1",
        "date": "2023-11-11",
        "timeSlot": "14:00-15:00",
        "status": "已签到",
        "checkinTime": datetime.now() - timedelta(hours=5),
        "createdAt": datetime.now() - timedelta(days=1),
        "updatedAt": datetime.now() - timedelta(hours=5),
    },
    {
        "id": "3",
        "seatId": "103",
        "seatNumber": "C3",
        "location": "图书馆三楼",
        "userId": "2",
        "date": "2023-11-12",
        "timeSlot": "19:00-20:00",
        "status": "已取消",
        "createdAt": datetime.now() - timedelta(days=3),
        "updatedAt": datetime.now() - timedelta(hours=12),
    },
    {
        "id": "4",
        "seatId": "104",
        "seatNumber": "D4",
        "location": "自习室",
        "userId": "1",
        "date": "2023-11-15",
        "timeSlot": "10:00-11:00",
        "status": "已预约",
        "createdAt": datetime.now() - timedelta(hours=6),
        "updatedAt": datetime.now() - timedelta(hours=6),
    }
]

# 座位模拟数据
MOCK_SEATS = [
    {
        "id": "101",
        "number": "A1",
        "location": "图书馆一楼",
        "status": "可用",
        "features": ["靠窗", "电源插座", "安静区"],
        "description": "靠窗座位，采光良好"
    },
    {
        "id": "102",
        "number": "B2",
        "location": "图书馆二楼",
        "status": "可用",
        "features": ["靠近书架", "电源插座"],
        "description": "靠近计算机科学书架"
    },
    {
        "id": "103",
        "number": "C3",
        "location": "图书馆三楼",
        "status": "维护中",
        "features": ["靠窗", "大桌面"],
        "description": "三人小组讨论座位"
    },
    {
        "id": "104",
        "number": "D4",
        "location": "自习室",
        "status": "已预约",
        "features": ["隔间", "电源插座", "网络接口"],
        "description": "独立隔间，适合长时间学习"
    },
    {
        "id": "105",
        "number": "E5",
        "location": "自习室",
        "status": "可用",
        "features": ["隔间", "电源插座"],
        "description": "安静独立空间"
    }
]

# 时间段模拟数据
MOCK_TIME_SLOTS = [
    {
        "id": "1",
        "slot": "09:00-10:00"
    },
    {
        "id": "2",
        "slot": "10:00-11:00"
    },
    {
        "id": "3",
        "slot": "11:00-12:00"
    },
    {
        "id": "4",
        "slot": "12:00-13:00"
    },
    {
        "id": "5",
        "slot": "13:00-14:00"
    },
    {
        "id": "6",
        "slot": "14:00-15:00"
    },
    {
        "id": "7",
        "slot": "15:00-16:00"
    },
    {
        "id": "8",
        "slot": "16:00-17:00"
    },
    {
        "id": "9",
        "slot": "17:00-18:00"
    },
    {
        "id": "10",
        "slot": "18:00-19:00"
    },
    {
        "id": "11",
        "slot": "19:00-20:00"
    },
    {
        "id": "12",
        "slot": "20:00-21:00"
    },
    {
        "id": "13",
        "slot": "21:00-22:00"
    }
]

# 房间模拟数据
MOCK_ROOMS = [
    {
        "id": "1",
        "name": "图书馆一楼",
        "capacity": 50,
        "location": "主校区",
        "is_active": True,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    },
    {
        "id": "2",
        "name": "图书馆二楼",
        "capacity": 40,
        "location": "主校区",
        "is_active": True,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    },
    {
        "id": "3",
        "name": "图书馆三楼",
        "capacity": 30,
        "location": "主校区",
        "is_active": True,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    },
    {
        "id": "4",
        "name": "自习室",
        "capacity": 20,
        "location": "东校区",
        "is_active": True,
        "created_at": "2023-01-01T00:00:00",
        "updated_at": "2023-01-01T00:00:00"
    }
]

# 位置模拟数据
MOCK_LOCATIONS = [
    {
        "id": "1",
        "name": "图书馆一楼"
    },
    {
        "id": "2",
        "name": "图书馆二楼"
    },
    {
        "id": "3",
        "name": "图书馆三楼"
    },
    {
        "id": "4",
        "name": "自习室"
    }
]

# 预约统计数据
MOCK_RESERVATION_STATS = [
    {"name": "图书馆一楼", "total": 10},
    {"name": "图书馆二楼", "total": 15},
    {"name": "图书馆三楼", "total": 8},
    {"name": "自习室", "total": 12}
]

# 签到统计数据
MOCK_CHECKIN_STATS = [
    {"name": "图书馆一楼", "total": 10, "checkedIn": 8},
    {"name": "图书馆二楼", "total": 15, "checkedIn": 12},
    {"name": "图书馆三楼", "total": 8, "checkedIn": 5},
    {"name": "自习室", "total": 12, "checkedIn": 9}
] 