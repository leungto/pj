"""
CRUD operations for the database models.
"""
from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any, Union
from datetime import datetime

from . import models


# ==================== 用户相关操作 ====================

def create_user(db: Session, username: str, email: str, hashed_password: str) -> models.User:
    """
    创建新用户
    
    Args:
        db: 数据库会话
        username: 用户名
        email: 电子邮件
        hashed_password: 哈希后的密码
        
    Returns:
        新创建的用户对象
    """
    db_user = models.User(
        username=username,
        email=email,
        hashed_password=hashed_password
    )
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def get_user(db: Session, user_id: int) -> Optional[models.User]:
    """
    通过ID获取用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        用户对象，如果不存在则返回None
    """
    return db.query(models.User).filter(models.User.id == user_id).first()


def get_user_by_email(db: Session, email: str) -> Optional[models.User]:
    """
    通过邮箱获取用户
    
    Args:
        db: 数据库会话
        email: 电子邮件
        
    Returns:
        用户对象，如果不存在则返回None
    """
    return db.query(models.User).filter(models.User.email == email).first()


def get_user_by_username(db: Session, username: str) -> Optional[models.User]:
    """
    通过用户名获取用户
    
    Args:
        db: 数据库会话
        username: 用户名
        
    Returns:
        用户对象，如果不存在则返回None
    """
    return db.query(models.User).filter(models.User.username == username).first()


def get_users(db: Session, skip: int = 0, limit: int = 100) -> List[models.User]:
    """
    获取用户列表
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的最大记录数
        
    Returns:
        用户对象列表
    """
    return db.query(models.User).offset(skip).limit(limit).all()


def update_user(db: Session, user_id: int, user_data: Dict[str, Any]) -> Optional[models.User]:
    """
    更新用户信息
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        user_data: 要更新的用户数据字典
        
    Returns:
        更新后的用户对象，如果用户不存在则返回None
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return None
        
    for key, value in user_data.items():
        if hasattr(db_user, key):
            setattr(db_user, key, value)
    
    db_user.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_user)
    return db_user


def delete_user(db: Session, user_id: int) -> bool:
    """
    删除用户
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        删除成功返回True，否则返回False
    """
    db_user = db.query(models.User).filter(models.User.id == user_id).first()
    if not db_user:
        return False
        
    db.delete(db_user)
    db.commit()
    return True


# ==================== 房间相关操作 ====================

def create_room(db: Session, name: str, location: str, capacity: int) -> models.Room:
    """
    创建新房间
    
    Args:
        db: 数据库会话
        name: 房间名称
        location: 房间位置
        capacity: 房间容量
        
    Returns:
        新创建的房间对象
    """
    db_room = models.Room(
        name=name,
        location=location,
        capacity=capacity
    )
    db.add(db_room)
    db.commit()
    db.refresh(db_room)
    return db_room


def get_room(db: Session, room_id: int) -> Optional[models.Room]:
    """
    通过ID获取房间
    
    Args:
        db: 数据库会话
        room_id: 房间ID
        
    Returns:
        房间对象，如果不存在则返回None
    """
    return db.query(models.Room).filter(models.Room.id == room_id).first()


def get_rooms(db: Session, skip: int = 0, limit: int = 100) -> List[models.Room]:
    """
    获取房间列表
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的最大记录数
        
    Returns:
        房间对象列表
    """
    return db.query(models.Room).filter(models.Room.is_active == True).offset(skip).limit(limit).all()


def update_room(db: Session, room_id: int, room_data: Dict[str, Any]) -> Optional[models.Room]:
    """
    更新房间信息
    
    Args:
        db: 数据库会话
        room_id: 房间ID
        room_data: 要更新的房间数据字典
        
    Returns:
        更新后的房间对象，如果房间不存在则返回None
    """
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return None
        
    for key, value in room_data.items():
        if hasattr(db_room, key):
            setattr(db_room, key, value)
    
    db_room.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_room)
    return db_room


def delete_room(db: Session, room_id: int) -> bool:
    """
    删除房间（软删除，将is_active设置为False）
    
    Args:
        db: 数据库会话
        room_id: 房间ID
        
    Returns:
        删除成功返回True，否则返回False
    """
    db_room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not db_room:
        return False
        
    db_room.is_active = False
    db_room.updated_at = datetime.utcnow()
    db.commit()
    return True


# ==================== 座位相关操作 ====================

def create_seat(db: Session, room_id: int, seat_number: str) -> models.Seat:
    """
    创建新座位
    
    Args:
        db: 数据库会话
        room_id: 房间ID
        seat_number: 座位编号
        
    Returns:
        新创建的座位对象
    """
    db_seat = models.Seat(
        room_id=room_id,
        seat_number=seat_number
    )
    db.add(db_seat)
    db.commit()
    db.refresh(db_seat)
    return db_seat


def get_seat(db: Session, seat_id: int) -> Optional[models.Seat]:
    """
    通过ID获取座位
    
    Args:
        db: 数据库会话
        seat_id: 座位ID
        
    Returns:
        座位对象，如果不存在则返回None
    """
    return db.query(models.Seat).filter(models.Seat.id == seat_id).first()


def get_seats_by_room(db: Session, room_id: int, skip: int = 0, limit: int = 100) -> List[models.Seat]:
    """
    获取指定房间的所有座位
    
    Args:
        db: 数据库会话
        room_id: 房间ID
        skip: 跳过的记录数
        limit: 返回的最大记录数
        
    Returns:
        座位对象列表
    """
    return db.query(models.Seat).filter(models.Seat.room_id == room_id).offset(skip).limit(limit).all()


def update_seat(db: Session, seat_id: int, seat_data: Dict[str, Any]) -> Optional[models.Seat]:
    """
    更新座位信息
    
    Args:
        db: 数据库会话
        seat_id: 座位ID
        seat_data: 要更新的座位数据字典
        
    Returns:
        更新后的座位对象，如果座位不存在则返回None
    """
    db_seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if not db_seat:
        return None
        
    for key, value in seat_data.items():
        if hasattr(db_seat, key):
            setattr(db_seat, key, value)
    
    db_seat.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_seat)
    return db_seat


def delete_seat(db: Session, seat_id: int) -> bool:
    """
    删除座位
    
    Args:
        db: 数据库会话
        seat_id: 座位ID
        
    Returns:
        删除成功返回True，否则返回False
    """
    db_seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if not db_seat:
        return False
        
    db.delete(db_seat)
    db.commit()
    return True


# ==================== 预订相关操作 ====================

def create_booking(
    db: Session, 
    user_id: int, 
    seat_id: int, 
    start_time: datetime, 
    end_time: datetime
) -> models.Booking:
    """
    创建新预订
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        seat_id: 座位ID
        start_time: 开始时间
        end_time: 结束时间
        
    Returns:
        新创建的预订对象
    """
    db_booking = models.Booking(
        user_id=user_id,
        seat_id=seat_id,
        start_time=start_time,
        end_time=end_time,
        status="pending"
    )
    db.add(db_booking)
    db.commit()
    db.refresh(db_booking)
    return db_booking


def get_booking(db: Session, booking_id: int) -> Optional[models.Booking]:
    """
    通过ID获取预订
    
    Args:
        db: 数据库会话
        booking_id: 预订ID
        
    Returns:
        预订对象，如果不存在则返回None
    """
    return db.query(models.Booking).filter(models.Booking.id == booking_id).first()


def get_user_bookings(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """
    获取用户的所有预订
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        skip: 跳过的记录数
        limit: 返回的最大记录数
        
    Returns:
        预订对象列表
    """
    return db.query(models.Booking).filter(models.Booking.user_id == user_id).offset(skip).limit(limit).all()


def get_seat_bookings(db: Session, seat_id: int, skip: int = 0, limit: int = 100) -> List[models.Booking]:
    """
    获取座位的所有预订
    
    Args:
        db: 数据库会话
        seat_id: 座位ID
        skip: 跳过的记录数
        limit: 返回的最大记录数
        
    Returns:
        预订对象列表
    """
    return db.query(models.Booking).filter(models.Booking.seat_id == seat_id).offset(skip).limit(limit).all()


def update_booking_status(db: Session, booking_id: int, status: str) -> Optional[models.Booking]:
    """
    更新预订状态
    
    Args:
        db: 数据库会话
        booking_id: 预订ID
        status: 新状态
        
    Returns:
        更新后的预订对象，如果预订不存在则返回None
    """
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not db_booking:
        return None
        
    db_booking.status = status
    db_booking.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_booking)
    return db_booking


def delete_booking(db: Session, booking_id: int) -> bool:
    """
    删除预订
    
    Args:
        db: 数据库会话
        booking_id: 预订ID
        
    Returns:
        删除成功返回True，否则返回False
    """
    db_booking = db.query(models.Booking).filter(models.Booking.id == booking_id).first()
    if not db_booking:
        return False
        
    db.delete(db_booking)
    db.commit()
    return True


# ==================== 预约相关操作 ====================

def create_reservation(
    db: Session, 
    user_id: int, 
    seat_id: int, 
    date: str, 
    time_slot_id: str
) -> models.Reservation:
    """
    创建新预约
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        seat_id: 座位ID
        date: 预约日期
        time_slot_id: 时间段ID
        
    Returns:
        新创建的预约对象
    """
    db_reservation = models.Reservation(
        user_id=user_id,
        seat_id=seat_id,
        date=date,
        time_slot_id=time_slot_id,
        status="待确认"
    )
    db.add(db_reservation)
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def get_reservation(db: Session, reservation_id: str) -> Optional[models.Reservation]:
    """
    通过ID获取预约
    
    Args:
        db: 数据库会话
        reservation_id: 预约ID
        
    Returns:
        预约对象，如果不存在则返回None
    """
    return db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()


def get_user_reservations(db: Session, user_id: int, skip: int = 0, limit: int = 100) -> List[models.Reservation]:
    """
    获取用户的所有预约
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        skip: 跳过的记录数
        limit: 返回的最大记录数
        
    Returns:
        预约对象列表
    """
    return db.query(models.Reservation).filter(models.Reservation.user_id == user_id).offset(skip).limit(limit).all()


def get_recent_reservations(db: Session, user_id: int, limit: int = 5) -> List[models.Reservation]:
    """
    获取用户最近的预约
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        limit: 返回的最大记录数
        
    Returns:
        预约对象列表
    """
    return db.query(models.Reservation)\
        .filter(models.Reservation.user_id == user_id)\
        .order_by(models.Reservation.created_at.desc())\
        .limit(limit)\
        .all()


def update_reservation_status(db: Session, reservation_id: str, status: str) -> Optional[models.Reservation]:
    """
    更新预约状态
    
    Args:
        db: 数据库会话
        reservation_id: 预约ID
        status: 新状态 ("待确认", "已确认", "已取消")
        
    Returns:
        更新后的预约对象，如果预约不存在则返回None
    """
    db_reservation = db.query(models.Reservation).filter(models.Reservation.id == reservation_id).first()
    if not db_reservation:
        return None
        
    db_reservation.status = status
    db_reservation.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_reservation)
    return db_reservation


def is_seat_reserved(db: Session, seat_id: int, date: str, time_slot_id: str) -> bool:
    """
    检查座位在指定时间段是否已被预约
    
    Args:
        db: 数据库会话
        seat_id: 座位ID
        date: 日期
        time_slot_id: 时间段ID
        
    Returns:
        如果座位已被预约返回True，否则返回False
    """
    reservation = db.query(models.Reservation).filter(
        models.Reservation.seat_id == seat_id,
        models.Reservation.date == date,
        models.Reservation.time_slot_id == time_slot_id,
        models.Reservation.status.in_(["待确认", "已确认"])
    ).first()
    
    return reservation is not None


def get_time_slot(db: Session, time_slot_id: str) -> Optional[models.TimeSlot]:
    """
    通过ID获取时间段
    
    Args:
        db: 数据库会话
        time_slot_id: 时间段ID
        
    Returns:
        时间段对象，如果不存在则返回None
    """
    return db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()


def create_time_slot(
    db: Session, 
    start_time: str,
    end_time: str,
    name: str,
    description: Optional[str] = None
) -> models.TimeSlot:
    """
    创建新时间段
    
    Args:
        db: 数据库会话
        start_time: 开始时间
        end_time: 结束时间
        name: 时间段名称
        description: 时间段描述
        
    Returns:
        新创建的时间段对象
    """
    db_time_slot = models.TimeSlot(
        start_time=start_time,
        end_time=end_time,
        name=name,
        description=description
    )
    db.add(db_time_slot)
    db.commit()
    db.refresh(db_time_slot)
    return db_time_slot


def get_time_slots(db: Session, skip: int = 0, limit: int = 100) -> List[models.TimeSlot]:
    """
    获取时间段列表
    
    Args:
        db: 数据库会话
        skip: 跳过的记录数
        limit: 返回的最大记录数
        
    Returns:
        时间段对象列表
    """
    return db.query(models.TimeSlot).filter(models.TimeSlot.is_active == True).offset(skip).limit(limit).all()


def update_time_slot(db: Session, time_slot_id: str, time_slot_data: Dict[str, Any]) -> Optional[models.TimeSlot]:
    """
    更新时间段信息
    
    Args:
        db: 数据库会话
        time_slot_id: 时间段ID
        time_slot_data: 要更新的时间段数据字典
        
    Returns:
        更新后的时间段对象，如果时间段不存在则返回None
    """
    db_time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()
    if not db_time_slot:
        return None
        
    for key, value in time_slot_data.items():
        if hasattr(db_time_slot, key):
            setattr(db_time_slot, key, value)
    
    db_time_slot.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_time_slot)
    return db_time_slot


def delete_time_slot(db: Session, time_slot_id: str) -> bool:
    """
    删除时间段（软删除，将is_active设置为False）
    
    Args:
        db: 数据库会话
        time_slot_id: 时间段ID
        
    Returns:
        删除成功返回True，否则返回False
    """
    db_time_slot = db.query(models.TimeSlot).filter(models.TimeSlot.id == time_slot_id).first()
    if not db_time_slot:
        return False
        
    db_time_slot.is_active = False
    db_time_slot.updated_at = datetime.utcnow()
    db.commit()
    return True


def get_reservation_stats(db: Session) -> List[Dict[str, Union[str, int]]]:
    """
    获取预约统计数据
    
    Args:
        db: 数据库会话
        
    Returns:
        统计数据列表，包含名称和总数
    """
    # 计算不同状态的预约数量
    result = []
    
    # 待确认预约数量
    pending_count = db.query(models.Reservation).filter(models.Reservation.status == "待确认").count()
    result.append({"name": "待确认预约", "total": pending_count})
    
    # 已确认预约数量
    confirmed_count = db.query(models.Reservation).filter(models.Reservation.status == "已确认").count()
    result.append({"name": "已确认预约", "total": confirmed_count})
    
    # 已取消预约数量
    cancelled_count = db.query(models.Reservation).filter(models.Reservation.status == "已取消").count()
    result.append({"name": "已取消预约", "total": cancelled_count})
    
    # 总预约数量
    total_count = db.query(models.Reservation).count()
    result.append({"name": "总预约数", "total": total_count})
    
    return result


def is_admin(db: Session, user_id: int) -> bool:
    """
    检查用户是否为管理员
    
    Args:
        db: 数据库会话
        user_id: 用户ID
        
    Returns:
        如果用户是管理员返回True，否则返回False
    """
    user = db.query(models.User).filter(models.User.id == user_id).first()
    return user is not None and user.is_admin 