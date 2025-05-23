"""
Reservation routes for the seat booking system.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from datetime import datetime, timedelta

from database.connection import get_db
from database import crud
from database.schemas import (
    ReservationCreate, 
    ReservationResponse, 
    ReservationDetailResponse,
    ReservationStatItem
)
from auth.dependencies import get_current_user_id
from mock_data.data import MOCK_RESERVATIONS, MOCK_RESERVATION_STATS, MOCK_CHECKIN_STATS

router = APIRouter()

@router.get("/user", response_model=List[ReservationResponse])
async def get_user_reservations(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取当前用户的所有预约
    """
    # 返回模拟数据
    return [r for r in MOCK_RESERVATIONS if r["userId"] == str(current_user_id)]

@router.get("/recent", response_model=List[ReservationResponse])
async def get_recent_reservations(
    limit: int = 5,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取用户最近的预约
    """
    # 返回模拟数据，按创建时间降序排列并限制数量
    user_reservations = [r for r in MOCK_RESERVATIONS if r["userId"] == str(current_user_id)]
    sorted_reservations = sorted(user_reservations, key=lambda x: x["createdAt"], reverse=True)
    return sorted_reservations[:limit]

@router.get("/today-checkin", response_model=List[ReservationResponse])
async def get_today_checkin_reservations(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取今日可签到的预约
    """
    # 返回模拟今日可签到的预约
    today = datetime.now().strftime("%Y-%m-%d")
    today = "2023-11-10"  # 为了确保有测试数据
    today_reservations = [
        r for r in MOCK_RESERVATIONS 
        if r["userId"] == str(current_user_id) and r["date"] == today and r["status"] == "已预约"
    ]
    return today_reservations

@router.get("/all/recent", response_model=List[ReservationResponse])
async def get_all_recent_reservations(
    limit: int = 5,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取所有最近的预约（管理员用）
    """
    # 返回模拟数据，按创建时间降序排列并限制数量
    sorted_reservations = sorted(MOCK_RESERVATIONS, key=lambda x: x["createdAt"], reverse=True)
    return sorted_reservations[:limit]

@router.get("/stats", response_model=List[ReservationStatItem])
async def get_reservation_stats(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取预约统计数据
    """
    # 返回模拟数据
    return MOCK_RESERVATION_STATS

@router.get("/checkin-stats", response_model=List)
async def get_checkin_stats(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取签到统计数据
    """
    # 返回模拟数据
    return MOCK_CHECKIN_STATS

@router.post("", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED)
async def create_reservation(
    reservation: ReservationCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    创建新预约
    """
    # 返回模拟新创建的预约
    new_reservation = {
        "id": "999",  # 假设这是新生成的ID
        "seatId": reservation.seatId,
        "seatNumber": f"S{reservation.seatId}",  # 模拟座位号
        "location": "新创建的预约位置",
        "userId": str(current_user_id),
        "date": str(reservation.date),
        "timeSlot": f"{reservation.timeSlotId}:00-{int(reservation.timeSlotId)+1}:00" if reservation.timeSlotId.isdigit() else "09:00-10:00",
        "status": "已预约",
        "createdAt": datetime.now(),
        "updatedAt": datetime.now(),
    }
    
    return new_reservation

@router.delete("/{reservation_id}", response_model=ReservationResponse)
async def cancel_reservation(
    reservation_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    取消预约
    """
    # 查找对应的预约
    reservation = next((r for r in MOCK_RESERVATIONS if r["id"] == reservation_id), None)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    # 验证预约是否属于当前用户
    if reservation["userId"] != str(current_user_id):
        raise HTTPException(status_code=403, detail="无权操作此预约")
    
    # 返回已取消的预约
    cancelled_reservation = {**reservation, "status": "已取消", "updatedAt": datetime.now()}
    return cancelled_reservation

@router.get("/{reservation_id}", response_model=ReservationDetailResponse)
async def get_reservation(
    reservation_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取预约详情
    """
    # 查找对应的预约
    reservation = next((r for r in MOCK_RESERVATIONS if r["id"] == reservation_id), None)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    # 验证预约是否属于当前用户
    if reservation["userId"] != str(current_user_id):
        raise HTTPException(status_code=403, detail="无权查看此预约")
    
    return reservation

@router.post("/{reservation_id}/checkin", response_model=ReservationResponse)
async def checkin_reservation(
    reservation_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    签到
    """
    # 查找对应的预约
    reservation = next((r for r in MOCK_RESERVATIONS if r["id"] == reservation_id), None)
    
    if not reservation:
        raise HTTPException(status_code=404, detail="预约不存在")
    
    if reservation["status"] != "已预约":
        raise HTTPException(status_code=400, detail="预约状态不允许签到")
    
    # 返回已签到的预约
    checked_in_reservation = {
        **reservation, 
        "status": "已签到", 
        "checkinTime": datetime.now().isoformat(),
        "updatedAt": datetime.now()
    }
    return checked_in_reservation