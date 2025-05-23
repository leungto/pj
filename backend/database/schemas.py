"""
Pydantic schemas for data validation.
"""
from datetime import datetime, date
from typing import List, Optional
from pydantic import BaseModel, EmailStr, Field, ConfigDict


# ==================== 用户相关模型 ====================

class UserBase(BaseModel):
    """用户基础模型"""
    username: str
    email: EmailStr


class UserCreate(UserBase):
    """创建用户模型"""
    password: str


class UserUpdate(BaseModel):
    """更新用户模型"""
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    is_active: Optional[bool] = None


class UserResponse(UserBase):
    """用户响应模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 房间相关模型 ====================

class RoomBase(BaseModel):
    """房间基础模型"""
    name: str
    location: str
    capacity: int


class RoomCreate(RoomBase):
    """创建房间模型"""
    pass


class RoomUpdate(BaseModel):
    """更新房间模型"""
    name: Optional[str] = None
    location: Optional[str] = None
    capacity: Optional[int] = None
    is_active: Optional[bool] = None


class RoomResponse(RoomBase):
    """房间响应模型"""
    id: int
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 座位相关模型 ====================

class SeatBase(BaseModel):
    """座位基础模型"""
    room_id: int
    seat_number: str


class SeatCreate(SeatBase):
    """创建座位模型"""
    pass


class SeatUpdate(BaseModel):
    """更新座位模型"""
    seat_number: Optional[str] = None
    is_available: Optional[bool] = None


class SeatResponse(SeatBase):
    """座位响应模型"""
    id: int
    is_available: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class SeatDetailResponse(SeatResponse):
    """座位详细响应模型，包含房间信息"""
    room: RoomResponse
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 预订相关模型 ====================

class BookingBase(BaseModel):
    """预订基础模型"""
    seat_id: int
    start_time: datetime
    end_time: datetime


class BookingCreate(BookingBase):
    """创建预订模型"""
    pass


class BookingUpdate(BaseModel):
    """更新预订模型"""
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    status: Optional[str] = None


class BookingResponse(BookingBase):
    """预订响应模型"""
    id: int
    user_id: int
    status: str
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True)


class BookingDetailResponse(BookingResponse):
    """预订详细响应模型，包含用户和座位信息"""
    user: UserResponse
    seat: SeatDetailResponse
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 预约相关模型 ====================

class ReservationCreate(BaseModel):
    """创建预约模型"""
    seatId: str
    date: date
    timeSlotId: str


class ReservationResponse(BaseModel):
    """预约响应模型"""
    id: str
    seatId: str
    seatNumber: str
    location: str
    userId: str
    date: str
    timeSlot: str
    status: str  # "待确认" | "已确认" | "已取消"
    createdAt: datetime
    updatedAt: datetime
    
    model_config = ConfigDict(from_attributes=True)


class ReservationDetailResponse(ReservationResponse):
    """预约详细响应模型，包含额外信息"""
    # 如果需要额外字段，可以在这里添加
    
    model_config = ConfigDict(from_attributes=True)


class ReservationStatItem(BaseModel):
    """预约统计项模型"""
    name: str
    total: int
    
    model_config = ConfigDict(from_attributes=True)


# ==================== 时间段相关模型 ====================

class TimeSlotBase(BaseModel):
    """时间段基础模型"""
    start_time: str  # 格式："HH:MM"
    end_time: str    # 格式："HH:MM"
    name: str        # 例如："上午", "下午"
    description: Optional[str] = None


class TimeSlotCreate(TimeSlotBase):
    """创建时间段模型"""
    pass


class TimeSlotUpdate(BaseModel):
    """更新时间段模型"""
    start_time: Optional[str] = None
    end_time: Optional[str] = None
    name: Optional[str] = None
    description: Optional[str] = None
    is_active: Optional[bool] = None


class TimeSlotResponse(TimeSlotBase):
    """时间段响应模型"""
    id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime
    
    model_config = ConfigDict(from_attributes=True) 