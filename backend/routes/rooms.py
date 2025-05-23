"""
Room and Location routes for the seat booking system.
"""
from typing import List
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from database.connection import get_db
from database import crud
from database.schemas import RoomCreate, RoomUpdate, RoomResponse
from auth.dependencies import get_current_user_id
from mock_data.data import MOCK_ROOMS, MOCK_LOCATIONS

router = APIRouter()

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """
    创建新房间
    """
    return crud.create_room(db=db, name=room.name, location=room.location, capacity=room.capacity)


@router.get("/", response_model=List[dict])
def get_all_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有房间
    """
    return MOCK_ROOMS


@router.get("/{room_id}", response_model=dict)
def get_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    获取特定房间信息
    """
    room = next((r for r in MOCK_ROOMS if r["id"] == room_id), None)
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")
    return room


@router.put("/{room_id}", response_model=RoomResponse)
def update_room(room_id: int, room: RoomUpdate, db: Session = Depends(get_db)):
    """
    更新房间信息
    """
    db_room = crud.update_room(db, room_id=room_id, room_data=room.dict(exclude_unset=True))
    if db_room is None:
        raise HTTPException(status_code=404, detail="房间不存在")
    return db_room


@router.delete("/{room_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_room(room_id: int, db: Session = Depends(get_db)):
    """
    删除房间（软删除）
    """
    result = crud.delete_room(db, room_id=room_id)
    if not result:
        raise HTTPException(status_code=404, detail="房间不存在")
    return None


# 添加一个端点来提供位置数据给前端使用
@router.get("/locations", response_model=List[dict], tags=["locations"])
def get_all_locations(
    db: Session = Depends(get_db)
):
    """
    获取所有位置
    """
    return MOCK_LOCATIONS 