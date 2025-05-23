"""
Time slots routes for the seat booking system.
"""
from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from database import crud
from database.schemas import TimeSlotCreate, TimeSlotUpdate, TimeSlotResponse
from auth.dependencies import get_current_user_id
from mock_data.data import MOCK_TIME_SLOTS

router = APIRouter()


@router.post("/", response_model=TimeSlotResponse, status_code=status.HTTP_201_CREATED)
def create_time_slot(time_slot: TimeSlotCreate, db: Session = Depends(get_db)):
    """
    创建新时间段
    """
    return crud.create_time_slot(
        db=db, 
        start_time=time_slot.start_time,
        end_time=time_slot.end_time,
        name=time_slot.name,
        description=time_slot.description
    )


@router.get("/", response_model=List[dict])
def get_all_time_slots(
    db: Session = Depends(get_db)
):
    """
    获取所有时间段
    """
    return MOCK_TIME_SLOTS


@router.get("/available", response_model=List[dict])
def get_available_time_slots(
    date: str,
    seatId: Optional[str] = None,
    db: Session = Depends(get_db)
):
    """
    获取可用时间段
    根据日期和座位ID获取可用的时间段
    """
    # 对于模拟数据，我们假设当前座位在指定日期的所有时间段都可用
    # 如果需要，可以添加更复杂的逻辑来模拟某些时间段已被预约
    
    if seatId == "104":  # 假设这个座位在某些时间段已被预约
        # 排除特定的小时时间段（例如下午的几个小时）
        return [slot for slot in MOCK_TIME_SLOTS if slot["id"] not in ["5", "6", "7", "8"]]  # 排除13:00-17:00的时间段
    
    return MOCK_TIME_SLOTS  # 返回所有时间段


@router.get("/{time_slot_id}", response_model=TimeSlotResponse)
def read_time_slot(time_slot_id: str, db: Session = Depends(get_db)):
    """
    获取特定时间段信息
    """
    db_time_slot = crud.get_time_slot(db, time_slot_id=time_slot_id)
    if db_time_slot is None:
        raise HTTPException(status_code=404, detail="时间段不存在")
    return db_time_slot


@router.put("/{time_slot_id}", response_model=TimeSlotResponse)
def update_time_slot(time_slot_id: str, time_slot: TimeSlotUpdate, db: Session = Depends(get_db)):
    """
    更新时间段信息
    """
    db_time_slot = crud.update_time_slot(
        db, 
        time_slot_id=time_slot_id, 
        time_slot_data=time_slot.dict(exclude_unset=True)
    )
    if db_time_slot is None:
        raise HTTPException(status_code=404, detail="时间段不存在")
    return db_time_slot


@router.delete("/{time_slot_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_time_slot(time_slot_id: str, db: Session = Depends(get_db)):
    """
    删除时间段
    """
    result = crud.delete_time_slot(db, time_slot_id=time_slot_id)
    if not result:
        raise HTTPException(status_code=404, detail="时间段不存在")
    return None
