"""
Booking routes for the seat booking system.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from database import crud
from database.schemas import BookingCreate, BookingUpdate, BookingResponse, BookingDetailResponse

router = APIRouter()


@router.post("/", response_model=BookingResponse, status_code=status.HTTP_201_CREATED)
def create_booking(booking: BookingCreate, user_id: int, db: Session = Depends(get_db)):
    """
    创建新预订
    """
    # 检查用户是否存在
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查座位是否存在
    seat = crud.get_seat(db, seat_id=booking.seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    
    # 检查座位是否可用
    if not seat.is_available:
        raise HTTPException(status_code=400, detail="座位不可用")
    
    # 创建预订
    return crud.create_booking(
        db=db, 
        user_id=user_id, 
        seat_id=booking.seat_id, 
        start_time=booking.start_time, 
        end_time=booking.end_time
    )


@router.get("/user/{user_id}", response_model=List[BookingResponse])
def read_user_bookings(user_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取用户的所有预订
    """
    # 检查用户是否存在
    user = crud.get_user(db, user_id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
        
    bookings = crud.get_user_bookings(db, user_id=user_id, skip=skip, limit=limit)
    return bookings


@router.get("/seat/{seat_id}", response_model=List[BookingResponse])
def read_seat_bookings(seat_id: int, skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    """
    获取座位的所有预订
    """
    # 检查座位是否存在
    seat = crud.get_seat(db, seat_id=seat_id)
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
        
    bookings = crud.get_seat_bookings(db, seat_id=seat_id, skip=skip, limit=limit)
    return bookings


@router.get("/{booking_id}", response_model=BookingDetailResponse)
def read_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    获取特定预订信息
    """
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="预订不存在")
    return db_booking


@router.put("/{booking_id}/status", response_model=BookingResponse)
def update_booking_status(booking_id: int, status: str, db: Session = Depends(get_db)):
    """
    更新预订状态
    """
    # 检查状态是否有效
    valid_statuses = ["pending", "confirmed", "cancelled", "completed"]
    if status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的状态，有效值为: {', '.join(valid_statuses)}")
    
    db_booking = crud.update_booking_status(db, booking_id=booking_id, status=status)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="预订不存在")
    return db_booking


@router.put("/{booking_id}", response_model=BookingResponse)
def update_booking(booking_id: int, booking: BookingUpdate, db: Session = Depends(get_db)):
    """
    更新预订信息
    """
    # 获取当前预订
    db_booking = crud.get_booking(db, booking_id=booking_id)
    if db_booking is None:
        raise HTTPException(status_code=404, detail="预订不存在")
    
    # 更新预订数据
    booking_data = booking.dict(exclude_unset=True)
    
    # 如果更新了状态，检查状态是否有效
    if "status" in booking_data:
        valid_statuses = ["pending", "confirmed", "cancelled", "completed"]
        if booking_data["status"] not in valid_statuses:
            raise HTTPException(status_code=400, detail=f"无效的状态，有效值为: {', '.join(valid_statuses)}")
    
    # 更新预订
    db_booking = crud.update_booking_status(db, booking_id=booking_id, status=booking_data.get("status", db_booking.status))
    return db_booking


@router.delete("/{booking_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_booking(booking_id: int, db: Session = Depends(get_db)):
    """
    删除预订
    """
    result = crud.delete_booking(db, booking_id=booking_id)
    if not result:
        raise HTTPException(status_code=404, detail="预订不存在")
    return None 