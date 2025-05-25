"""
Seat routes for the seat booking system.
"""
import json
from typing import List, Optional
from datetime import datetime, date
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from database import crud
from database.schemas import SeatCreate, SeatUpdate, SeatResponse, SeatDetailResponse
from auth.dependencies import get_current_user_id
from sqlalchemy.orm import Session,joinedload
from mock_data.data import MOCK_SEATS
import database.models as models   
import ast
router = APIRouter()

def structure_seat_data(seat):
    features = ast.literal_eval(seat.features)
    return {
        "id": str(seat.id),
        "roomId": seat.room_id,
        "location": seat.room.name,
        "number": seat.seat_number,
        "status": "可用" if seat.is_available == 1 else "维护中",
        "features": features,
        "description": seat.description,
        "createdAt": seat.created_at.isoformat(),
        "updatedAt": seat.updated_at.isoformat()
    }

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
    # new_id = str(int(MOCK_SEATS[-1]["id"]) + 1)
    
    # 创建新座位
    new_seat = {
        "number": data.get("number", ),
        "location": data.get("locationId", "默认位置"),
        "status": "可用",
        "features": data.get("features"),
        "description": data.get("description", "")
    }
    # print(new_seat)
    # print(data.get("status"))
    new_seat = models.Seat(
        room_id=data.get("locationId"),
        seat_number=data.get("number"),
        is_available=1,
        features=str(data.get("features")),
        description=data.get("description", ""),
    )
    db.add(new_seat)
    db.commit()
    db.refresh(new_seat)

    return structure_seat_data(new_seat)



@router.get("/", response_model=List[dict])
def get_all_seats(
    db: Session = Depends(get_db)
):
    """
    获取所有座位
    """
    seats = db.query(models.Seat).all()
    # 转换为字典列表
    seat_list = [
        structure_seat_data(seat)
        for seat in seats
    ]
    # print(seat_list)
    # print(MOCK_SEATS)
    return seat_list


@router.get("/available", response_model=List[dict])
def get_available_seats(
    date: str,
    timeSlotId: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取可用座位
    """
    # 返回状态为"可用"的座位\
    seats = db.query(models.Seat).all()
    seat_list = [
        structure_seat_data(seat)
        for seat in seats
    ]
    available_seats = [seat for seat in seat_list if seat["status"] == "可用"]
    return available_seats


@router.get("/{seat_id}", response_model=dict)
def get_seat(
    seat_id: str,
    db: Session = Depends(get_db)
):
    """
    获取特定座位信息
    """
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    return structure_seat_data(seat)


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
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    print(data.get("status"))
    # 更新状态
    seat.is_available = 1 if data.get("status") == "可用" else 0
    seat.updated_at = datetime.now()
    db.commit()
    db.refresh(seat)
    return structure_seat_data(seat)


@router.delete("/{seat_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_seat(
    seat_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    删除座位
    """
    seat = db.query(models.Seat).filter(models.Seat.id == seat_id).first()
    if not seat:
        raise HTTPException(status_code=404, detail="座位不存在")
    
    # 在真实实现中，这里会从数据库中删除座位
    db.delete(seat)
    db.commit()
    # db.refresh(seat)
    # 对于模拟数据，我们只返回成功状态码
    return None 