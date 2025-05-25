"""
Database models for the seat booking system.
"""
from datetime import datetime
import uuid
from sqlalchemy import Column, Integer, String, DateTime, Boolean, ForeignKey, Date
from sqlalchemy.orm import relationship

from .connection import Base


class User(Base):
    """用户模型"""
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)
    is_admin = Column(Boolean, default=False)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：一个用户可以有多个预订
    bookings = relationship("Booking", back_populates="user")
    # 关系：一个用户可以有多个预约
    reservations = relationship("Reservation", back_populates="user")


class Room(Base):
    """房间模型"""
    __tablename__ = "rooms"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    location = Column(String)
    capacity = Column(Integer)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：一个房间可以有多个座位
    seats = relationship("Seat", back_populates="room")


class Seat(Base):
    """座位模型"""
    __tablename__ = "seats"

    id = Column(Integer, primary_key=True, index=True)
    room_id = Column(Integer, ForeignKey("rooms.id"))
    seat_number = Column(String, index=True)
    is_available = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：一个座位属于一个房间
    room = relationship("Room", back_populates="seats")
    # 关系：一个座位可以有多个预订
    bookings = relationship("Booking", back_populates="seat")
    # 关系：一个座位可以有多个预约
    reservations = relationship("Reservation", back_populates="seat")


class Booking(Base):
    """预订模型"""
    __tablename__ = "bookings"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    start_time = Column(DateTime)
    end_time = Column(DateTime)
    status = Column(String, default="pending")  # pending, confirmed, cancelled, completed
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：一个预订属于一个用户
    user = relationship("User", back_populates="bookings")
    # 关系：一个预订属于一个座位
    seat = relationship("Seat", back_populates="bookings")


class TimeSlot(Base):
    """时间段模型"""
    __tablename__ = "time_slots"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    start_time = Column(String, nullable=False)  # 格式："HH:MM"
    end_time = Column(String, nullable=False)    # 格式："HH:MM"
    name = Column(String, nullable=False)        # 例如："上午", "下午"
    description = Column(String, nullable=True)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：一个时间段可以有多个预约
    reservations = relationship("Reservation", back_populates="time_slot")


class Reservation(Base):
    """预约模型"""
    __tablename__ = "reservations"

    id = Column(String, primary_key=True, default=lambda: str(uuid.uuid4()))
    user_id = Column(Integer, ForeignKey("users.id"))
    seat_id = Column(Integer, ForeignKey("seats.id"))
    date = Column(Date, nullable=False)           # 预约日期
    time_slot_id = Column(String, ForeignKey("time_slots.id"))
    status = Column(String, default="待确认")     # 待确认, 已确认, 已取消
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    # 关系：一个预约属于一个用户
    user = relationship("User", back_populates="reservations")
    # 关系：一个预约属于一个座位
    seat = relationship("Seat", back_populates="reservations")
    # 关系：一个预约属于一个时间段
    time_slot = relationship("TimeSlot", back_populates="reservations")
