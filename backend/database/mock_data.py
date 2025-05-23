"""
生成座位预约系统的模拟数据
"""
import random
from datetime import datetime, timedelta, date
from sqlalchemy.orm import Session

from . import models, create_tables
from .connection import get_db
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


def create_mock_reservations(db: Session, num_reservations=20):
    """
    创建模拟预约数据
    """
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
    
    for _ in range(num_reservations):
        user = random.choice(users)
        seat = random.choice(seats)
        time_slot = random.choice(time_slots)
        reservation_date = random.choice(date_range)
        status = random.choice(statuses)
        
        # 检查该座位在该时间段是否已被预约
        if not crud.is_seat_reserved(db, seat_id=seat.id, date=reservation_date, time_slot_id=time_slot.id):
            reservation = models.Reservation(
                user_id=user.id,
                seat_id=seat.id,
                date=reservation_date,
                time_slot_id=time_slot.id,
                status=status,
                created_at=datetime.utcnow() - timedelta(days=random.randint(0, 7))
            )
            db.add(reservation)
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
    
    try:
        # 创建时间段
        time_slots = create_mock_time_slots(db)
        
        # 创建预约
        create_mock_reservations(db)
        
        print("模拟数据创建成功")
        
    except Exception as e:
        print(f"创建模拟数据时出错: {e}")
    finally:
        db.close()


if __name__ == "__main__":
    create_mock_data() 