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
import database.models as models   

router = APIRouter()

@router.post("/", response_model=RoomResponse, status_code=status.HTTP_201_CREATED)
def create_room(room: RoomCreate, db: Session = Depends(get_db)):
    """
    创建新房间
    """
    return crud.create_room(db=db, name=room.name, location=room.location, capacity=room.capacity)

def structure_room_data(room):
    return {
        "id": str(room.id),
        "name": room.name,
        "location": room.location,
        "capacity": room.capacity,
        "is_active": room.is_active,
        "createdAt": room.created_at.isoformat(),
        "updatedAt": room.updated_at.isoformat()
    }
@router.get("/", response_model=List[dict])
def get_all_rooms(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    获取所有房间
    """
    rooms = db.query(models.Room).all()
    if not rooms:
        raise HTTPException(status_code=404, detail="没有房间信息")
    # 这里可以根据需要进行数据处理
    room_list = [structure_room_data(room) for room in rooms]

    return room_list


@router.get("/{room_id}", response_model=dict)
def get_room(
    room_id: str,
    db: Session = Depends(get_db)
):
    """
    获取特定房间信息
    """
    room = db.query(models.Room).filter(models.Room.id == room_id).first()
    if not room:
        raise HTTPException(status_code=404, detail="房间不存在")
    return structure_room_data(room)


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
    locations = (
        db.query(models.Room.location)
        .distinct()
        .order_by(models.Room.location)
        .all()
    )
    # 生成自增 id（从 1 开始）
    return [{"id": idx+1, "name": loc[0]} for idx, loc in enumerate(locations)]
