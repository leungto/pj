"""
Seat routes for the seat booking system.
"""
from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from database import crud
from database.schemas import SeatCreate, SeatUpdate, SeatResponse, SeatDetailResponse
from auth.dependencies import get_current_user_id
from mock_data.data import MOCK_SEATS

router = APIRouter()

@router.post("/", response_model=dict, status_code=status.HTTP_201_CREATED)
def create_seat(
    data: dict,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    创建新座位
    """
    # 生成一个新ID
    new_id = str(int(MOCK_SEATS[-1]["id"]) + 1)
    
    # 创建新座位
    new_seat = {
        "id": new_id,
        "number": data.get("number", f"NewSeat{new_id}"),
        "location": data.get("locationId", "默认位置"),
        "status": "可用",
        "features": data.get("features", []),
        "description": data.get("description", "")
    }
    
    return new_seat


@router.get("/", response_model=List[dict])
def get_all_seats(
    db: Session = Depends(get_db)
):
    """
    获取所有座位
    """
    return MOCK_SEATS


@router.get("/available", response_model=List[dict])
def get_available_seats(
    date: str,
    timeSlotId: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取可用座位
    """
    # 返回状态为"可用"的座位
    available_seats = [seat for seat in MOCK_SEATS if seat["status"] == "可用"]
    return available_seats


@router.get("/{seat_id}", response_model=dict)
def get_seat(
    seat_id: str,
    db: Session = Depends(get_db)
):
    """
    获取特定座位信息
    """
    seat = next((s for s in MOCK_SEATS if s["id"] == seat_id), None)
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    return seat


@router.patch("/{seat_id}/status", response_model=dict)
def update_seat_status(
    seat_id: str,
    data: dict,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    更新座位状态
    """
    seat = next((s for s in MOCK_SEATS if s["id"] == seat_id), None)
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    
    # 更新状态
    updated_seat = {**seat, "status": data.get("status", seat["status"])}
    return updated_seat


@router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seat(
    seat_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    删除座位
    """
    seat = next((s for s in MOCK_SEATS if s["id"] == seat_id), None)
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    
    # 在真实实现中，这里会从数据库中删除座位
    # 对于模拟数据，我们只返回成功状态码
    return None 