"""
生成座位预约系统的模拟数据
"""
import random
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session

from . import models, create_tables
from database.connection import get_db
from . import crud


def create_mock_time_slots(db: Session):
    """
    创建模拟时间段数据
    """
    time_slots = [
        {
            "start_time": "08:00",
            "end_time": "10:00",
            "name": "上午场次1",
            "description": "适合早起的人"
        },
        {
            "start_time": "10:30",
            "end_time": "12:30",
            "name": "上午场次2",
            "description": "午餐前的黄金时段"
        },
        {
            "start_time": "13:30",
            "end_time": "15:30",
            "name": "下午场次1",
            "description": "午休后精力充沛的时段"
        },
        {
            "start_time": "16:00",
            "end_time": "18:00",
            "name": "下午场次2",
            "description": "傍晚时分安静的学习时段"
        },
        {
            "start_time": "19:00",
            "end_time": "21:00",
            "name": "晚间场次",
            "description": "适合夜间学习的人"
        }
    ]
    
    db_time_slots = []
    for time_slot_data in time_slots:
        # 检查时间段是否已存在
        existing = db.query(models.TimeSlot).filter(
            models.TimeSlot.start_time == time_slot_data["start_time"],
            models.TimeSlot.end_time == time_slot_data["end_time"]
        ).first()
        
        if not existing:
            time_slot = models.TimeSlot(**time_slot_data)
            db.add(time_slot)
            db_time_slots.append(time_slot)
    
    if db_time_slots:
        db.commit()
        for time_slot in db_time_slots:
            db.refresh(time_slot)
        print(f"创建了 {len(db_time_slots)} 个时间段")
    else:
        print("时间段已存在，无需创建")
    
    return db.query(models.TimeSlot).all()


def create_mock_rooms(db: Session):
    """
    创建模拟房间数据
    """
    rooms = [
    {
        "name": "图书馆一楼",
        "capacity": 50,
        "location": "主校区",
        "is_active": True,
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1)
    },
    {
        "name": "图书馆二楼",
        "capacity": 40,
        "location": "主校区",
        "is_active": True,
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1)
    },
    {
        "name": "图书馆三楼",
        "capacity": 30,
        "location": "主校区",
        "is_active": True,
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1)
    },
    {
        "name": "自习室",
        "capacity": 20,
        "location": "东校区",
        "is_active": True,
        "created_at": datetime(2023, 1, 1),
        "updated_at": datetime(2023, 1, 1)
    }
    ]

    db_rooms = []
    for room in rooms:
        db_room = models.Room(**room)
        db.add(db_room)
        db_rooms.append(db_room)

    if db_rooms:
        db.commit()
        for room in db_rooms:
            db.refresh(room)
        print(f"创建了 {len(db_rooms)} 个房间")

    return db.query(models.Room).all()

def create_mock_seats(db: Session):
    """
    创建模拟座位数据
    """
    seats = [
    {
        "seat_number": "A1",
        "room_id": 1,
        "is_available": 1,
        "features": "['靠窗', '电源插座', '安静区']",
        "description": "靠窗座位，采光良好"
    },
    {
        "seat_number": "B2",
        "room_id": 2,
        "is_available": 1,
        "features": "['靠近书架', '电源插座']",
        "description": "靠近计算机科学书架"
    },
    {
        "seat_number": "C3",
        "room_id": 1,
        "is_available": 0,
        "features": "['靠窗', '大桌面']",
        "description": "三人小组讨论座位"
    },
    {
        "seat_number": "D4",
        "room_id": 2,
        "is_available": 2,
        "features": "['隔间', '电源插座', '网络接口']",
        "description": "独立隔间，适合长时间学习"
    },
    {
        "seat_number": "E5",
        "room_id": 1,
        "is_available":1,
        "features": "['隔间', '电源插座']",
        "description": "安静独立空间"
    }
    ]

    db_seats = []
    for seat in seats:
        db_seat = models.Seat(**seat)
        db.add(db_seat)
        db_seats.append(db_seat)

    if db_seats:
        db.commit()
        for seat in db_seats:
            db.refresh(seat)
        print(f"创建了 {len(db_seats)} 个座位")

    return db.query(models.Seat).all()

def create_mock_reservations(db: Session):
    """
    创建模拟预约数据
    """
    reservations = [
        {
            "id": "1",
            "seatId": "101",
            "seatNumber": "A1",
            "location": "图书馆一楼",
            "userId": "1",
            "date": datetime(2023, 1, 1),
            # "timeSlot": "09:00-10:00",
            "timeSlotId": "1",
            "status": "已预约",
            "createdAt": datetime(2023, 1, 1),
            "updatedAt": datetime(2023, 1, 1),
        },
        {
            "id": "2",
            "seatId": "102",
            "seatNumber": "B2",
            "location": "图书馆二楼",
            "userId": "1",
            "date": datetime(2023, 1, 1),
            # "timeSlot": "14:00-15:00",
            "timeSlotId": "2",
            "status": "已签到",
            "checkinTime": datetime(2023, 1, 1,8),
            "createdAt": datetime(2023, 1, 1),
            "updatedAt": datetime(2023, 1, 1),
        },
        {
            "id": "3",
            "seatId": "103",
            "seatNumber": "C3",
            "location": "图书馆三楼",
            "userId": "2",
            "date": datetime(2023, 1, 1),
            # "timeSlot": "19:00-20:00",
            "timeSlotId": "3",
            "status": "已取消",
            "createdAt": datetime(2023, 1, 1),
            "updatedAt": datetime(2023, 1, 1),
        },
        {
            "id": "4",
            "seatId": "104",
            "seatNumber": "D4",
            "location": "自习室",
            "userId": "1",
            "date": datetime(2023, 1, 1),
            # "timeSlot": "10:00-11:00",
            "timeSlotId": "1",
            "status": "已预约",
            "createdAt": datetime(2023, 1, 1),
            "updatedAt": datetime(2023, 1, 1),
        }
    ]

    # 获取所有用户、座位和时间段
    users = db.query(models.User).all()
    seats = db.query(models.Seat).all()
    time_slots = db.query(models.TimeSlot).all()
    
    if not users:
        print("没有用户数据，请先创建用户")
        return
    
    if not seats:
        print("没有座位数据，请先创建座位")
        return
    
    if not time_slots:
        print("没有时间段数据，请先创建时间段")
        return
    
    # 生成预约的日期范围（未来两周内）
    today = date.today()
    date_range = [(today + timedelta(days=i)).isoformat() for i in range(1, 15)]
    
    # 可能的预约状态
    statuses = ["待确认", "已确认", "已取消"]
    
    # 创建预约
    reservations_created = 0
    
    for reservation in reservations:
        # user = random.choice(users)
        # seat = random.choice(seats)
        # time_slot = random.choice(time_slots)
        # reservation_date = random.choice(date_range)
        # status = random.choice(statuses)
        
        # 检查该座位在该时间段是否已被预约
        print(reservation)
        if not crud.is_seat_reserved(db, seat_id=reservation["seatId"], date=reservation["date"], time_slot_id=reservation["timeSlotId"]):
            res = models.Reservation(
                user_id=reservation["userId"],
                seat_id=reservation["seatId"],
                date=reservation["date"],
                time_slot_id=reservation["timeSlotId"],
                status=reservation["status"],
                created_at=reservation["createdAt"],
                updated_at=reservation["updatedAt"]
            )
            db.add(res)
            reservations_created += 1
    
    db.commit()
    print(f"创建了 {reservations_created} 个预约")


def create_mock_data():
    """
    创建所有模拟数据
    """
    # 创建数据库表
    create_tables()
    
    # 获取数据库会话
    db = next(get_db())
    
    # try:
    # 创建时间段
    print("okk")
    time_slots = create_mock_time_slots(db)
    print("hello")
    # 创建预约
    create_mock_rooms(db)
    create_mock_seats(db)
    create_mock_reservations(db)
    print("~~~~")
    
    
    print("模拟数据创建成功")
        
    # except Exception as e:
    #     print(f"创建模拟数据时出错: {e}")
    # finally:
    #     db.close()


if __name__ == "__main__":
    create_mock_data() 