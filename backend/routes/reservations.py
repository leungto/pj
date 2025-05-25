"""
Reservation routes for the seat booking system.
"""

from typing import List, Optional
from fastapi import APIRouter, Depends, HTTPException, status, Request
from sqlalchemy.orm import Session
from sqlalchemy import func
from datetime import datetime, timedelta, date

from database.connection import get_db
from database import crud
from database.schemas import (
    ReservationCreate,
    ReservationResponse,
    ReservationDetailResponse,
    ReservationStatItem,
)
from auth.dependencies import get_current_user_id
from mock_data.data import MOCK_RESERVATIONS, MOCK_RESERVATION_STATS, MOCK_CHECKIN_STATS

from database import models

router = APIRouter()


@router.get("/user", response_model=List[ReservationResponse])
async def get_user_reservations(
    current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """
    获取当前用户的所有预约
    """
    print("🌳 def get_user_reservations")

    # 返回模拟数据
    # 查询数据库中的预约数据
    reservations_current_user = (
        db.query(models.Reservation)
        .filter(models.Reservation.user_id == current_user_id)
        .all()
    )
    print(reservations_current_user[0] if len(reservations_current_user) > 0 else None)

    start_time = [
        db.query(models.TimeSlot.start_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in reservations_current_user
    ]

    end_time = [
        db.query(models.TimeSlot.end_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in reservations_current_user
    ]

    seats = [
        db.query(models.Seat).filter(models.Seat.id == reservation.seat_id).first()
        for reservation in reservations_current_user
    ]

    rooms = [
        db.query(models.Room).filter(models.Room.id == seat.room_id).first()
        for seat in seats
    ]

    response_data = [
        {
            "id": reservation.id,
            "seatId": str(reservation.seat_id),
            "seatNumber": f"{seat.seat_number}",  # 模拟座位号
            "location": f"{room.name}({room.location})",  # 模拟位置
            "userId": str(reservation.user_id),
            "date": reservation.date.strftime("%Y-%m-%d"),  # 转换为字符串
            # "timeSlot": (
            #     f"{reservation.time_slot_id}:00-{int(reservation.time_slot_id)+1}:00"
            #     if reservation.time_slot_id.isdigit()
            #     else "09:00-10:00"
            # ),
            "timeSlot": f"{st[0]}-{et[0]}",
            "status": reservation.status,
            "createdAt": datetime.fromisoformat(reservation.created_at.isoformat()),
            "updatedAt": datetime.fromisoformat(reservation.updated_at.isoformat()),
        }
        for st, et, seat, room, reservation in zip(
            start_time, end_time, seats, rooms, reservations_current_user
        )
    ]

    return response_data
    # return [r for r in MOCK_RESERVATIONS if r["userId"] == str(current_user_id)]


@router.get("/recent", response_model=List[ReservationResponse])
async def get_recent_reservations(
    limit: int = 5,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    获取用户最近的预约
    """

    sorted_reservations = (
        db.query(models.Reservation)
        .filter(models.Reservation.user_id == current_user_id)
        .order_by(models.Reservation.created_at.desc())
        .limit(limit)
        .all()
    )

    start_time = [
        db.query(models.TimeSlot.start_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in sorted_reservations
    ]

    end_time = [
        db.query(models.TimeSlot.end_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in sorted_reservations
    ]

    seats = [
        db.query(models.Seat).filter(models.Seat.id == reservation.seat_id).first()
        for reservation in sorted_reservations
    ]

    rooms = [
        db.query(models.Room).filter(models.Room.id == seat.room_id).first()
        for seat in seats
    ]

    # print(sorted_reservations)
    # reservation = sorted_reservations[0]
    # 转换为符合 ReservationResponse 的格式
    response_data = [
        {
            "id": reservation.id,
            "seatId": str(reservation.seat_id),
            "seatNumber": f"{seat.seat_number}",  # 模拟座位号
            "location": f"{room.name}({room.location})",  # 模拟位置
            "userId": str(reservation.user_id),
            "date": reservation.date.strftime("%Y-%m-%d"),  # 转换为字符串
            # "timeSlot": (
            #     f"{reservation.time_slot_id}:00-{int(reservation.time_slot_id)+1}:00"
            #     if reservation.time_slot_id.isdigit()
            #     else "09:00-10:00"
            # ),
            "timeSlot": f"{st[0]}-{et[0]}",
            "status": reservation.status,
            "createdAt": datetime.fromisoformat(reservation.created_at.isoformat()),
            "updatedAt": datetime.fromisoformat(reservation.updated_at.isoformat()),
        }
        for st, et, seat, room, reservation in zip(
            start_time, end_time, seats, rooms, sorted_reservations
        )
    ]
    # print("❌")
    # print(response_data[0])

    # # 返回模拟数据，按创建时间降序排列并限制数量
    # user_reservations = [
    #     r for r in MOCK_RESERVATIONS if r["userId"] == str(current_user_id)
    # ]

    # sorted_reservations = sorted(
    #     user_reservations, key=lambda x: x["createdAt"], reverse=True
    # )
    # print(MOCK_RESERVATIONS[0])

    return response_data


@router.get("/today-checkin", response_model=List[ReservationResponse])
async def get_today_checkin_reservations(
    current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """
    获取今日可签到的预约
    """
    # 返回模拟今日可签到的预约
    today = "2023-11-10"  # 为了确保有测试数据
    today = datetime.now().strftime("%Y-%m-%d")
    # today_reservations = [
    #     r
    #     for r in MOCK_RESERVATIONS
    #     if r["userId"] == str(current_user_id)
    #     and r["date"] == today
    #     and r["status"] == "已预约"
    # ]
    today_reservations = (
        db.query(models.Reservation)
        .filter(
            models.Reservation.user_id == current_user_id,
            models.Reservation.date == today,
            models.Reservation.status == "已预约",
        )
        .all()
    )

    start_time = [
        db.query(models.TimeSlot.start_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in today_reservations
    ]

    end_time = [
        db.query(models.TimeSlot.end_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in today_reservations
    ]

    response_data = [
        {
            "id": reservation.id,
            "seatId": str(reservation.seat_id),
            "seatNumber": f"S{reservation.seat_id}",  # 模拟座位号
            "location": "预约位置",  # 模拟位置
            "userId": str(reservation.user_id),
            "date": reservation.date.strftime("%Y-%m-%d"),  # 转换为字符串
            # "timeSlot": (
            #     f"{reservation.time_slot_id}:00-{int(reservation.time_slot_id)+1}:00"
            #     if reservation.time_slot_id.isdigit()
            #     else "09:00-10:00"
            # ),
            "timeSlot": f"{st[0]}-{et[0]}",
            "status": reservation.status,
            "createdAt": datetime.fromisoformat(reservation.created_at.isoformat()),
            "updatedAt": datetime.fromisoformat(reservation.updated_at.isoformat()),
        }
        for st, et, reservation in zip(start_time, end_time, today_reservations)
    ]

    # return today_reservations
    return response_data


@router.get("/all/recent", response_model=List[ReservationResponse])
async def get_all_recent_reservations(
    limit: int = 5,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    获取所有最近的预约（管理员用）
    """
    # 返回模拟数据，按创建时间降序排列并限制数量
    sorted_reservations = sorted(
        MOCK_RESERVATIONS, key=lambda x: x["createdAt"], reverse=True
    )
    sorted_reservations = (
        db.query(models.Reservation)
        .order_by(models.Reservation.created_at.desc())
        .limit(limit)
        .all()
    )

    start_time = [
        db.query(models.TimeSlot.start_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in sorted_reservations
    ]

    end_time = [
        db.query(models.TimeSlot.end_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
        for reservation in sorted_reservations
    ]

    seats = [
        db.query(models.Seat).filter(models.Seat.id == reservation.seat_id).first()
        for reservation in sorted_reservations
    ]

    rooms = [
        db.query(models.Room).filter(models.Room.id == seat.room_id).first()
        for seat in seats
    ]

    response_data = [
        {
            "id": reservation.id,
            "seatId": str(reservation.seat_id),
            "seatNumber": f"{seat.seat_number}",  # 模拟座位号
            "location": f"{room.name}({room.location})",  # 模拟位置
            "userId": str(reservation.user_id),
            "date": reservation.date.strftime("%Y-%m-%d"),  # 转换为字符串
            # "timeSlot": (
            #     f"{reservation.time_slot_id}:00-{int(reservation.time_slot_id)+1}:00"
            #     if reservation.time_slot_id.isdigit()
            #     else "09:00-10:00"
            # ),
            "timeSlot": f"{st[0]}-{et[0]}",
            "status": reservation.status,
            "createdAt": datetime.fromisoformat(reservation.created_at.isoformat()),
            "updatedAt": datetime.fromisoformat(reservation.updated_at.isoformat()),
        }
        for st, et, seat, room, reservation in zip(
            start_time, end_time, seats, rooms, sorted_reservations
        )
    ]
    # print("❌")
    # print(response_data[0])

    # return sorted_reservations[:limit]
    return response_data


@router.get("/checkin-stats", response_model=List)
async def get_checkin_stats(
    current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """
    获取签到统计数据
    """
    # 返回模拟数据

    # checkin_stats = (
    #     db.query(
    #         models.Room.name.label("location"),  # 获取房间名称作为 location
    #         func.count(models.Reservation.id).label("total"),  # 统计每个位置的预约总数
    #         func.sum(
    #             func.case([(models.Reservation.status == "已签到", 1)], 0)  # 默认值为 0
    #         ).label(
    #             "checkedIn"
    #         ),  # 统计每个位置的已签到数量
    #     )
    #     .join(
    #         models.Seat, models.Reservation.seat_id == models.Seat.id
    #     )  # 关联 seats 表
    #     .join(models.Room, models.Seat.room_id == models.Room.id)  # 关联 rooms 表
    #     .group_by(models.Room.name)  # 按房间名称分组
    #     .all()
    # )

    # 第一步：查询所有预约记录
    reservations = db.query(
        models.Reservation.id, models.Reservation.seat_id, models.Reservation.status
    ).all()

    # 第二步：获取 seat_id 对应的 room_id
    seat_to_room = {
        seat.id: seat.room_id
        for seat in db.query(models.Seat.id, models.Seat.room_id).all()
    }

    # 第三步：获取 room_id 对应的 location 信息
    room_to_location = {
        room.id: room.name for room in db.query(models.Room.id, models.Room.name).all()
    }

    # 初始化统计数据，确保所有 location 都有默认值
    stats = {
        location: {"total": 0, "checkedIn": 0} for location in room_to_location.values()
    }

    # 第四步：统计每个 location 的预约总数和已签到数量
    for reservation in reservations:
        seat_id = reservation.seat_id
        room_id = seat_to_room.get(seat_id)
        location = room_to_location.get(room_id)

        if location not in stats:
            stats[location] = {"total": 0, "checkedIn": 0}

        stats[location]["total"] += 1
        if reservation.status == "已签到":
            stats[location]["checkedIn"] += 1

    # 转换为列表格式
    response_data = [
        {"name": location, "total": data["total"], "checkedIn": data["checkedIn"]}
        for location, data in stats.items()
    ]
    # response_data = [
    #     {
    #         "name": response.location,
    #         "total": response.total,
    #         "checkedIn": response.checkedIn,
    #     }
    #     for response in checkin_stats
    # ]
    return response_data


@router.get("/stats", response_model=List[ReservationStatItem])
async def get_reservation_stats(
    current_user_id: int = Depends(get_current_user_id), db: Session = Depends(get_db)
):
    """
    获取预约统计数据
    """
    # 查询数据库中的预约统计数据
    # 查询数据库中的预约统计数据
    reservation_stats = (
        db.query(
            models.Room.name.label("location"),  # 获取房间名称作为 location
            func.count(models.Reservation.id).label("total"),  # 统计每个位置的预约总数
        )
        .join(
            models.Seat, models.Reservation.seat_id == models.Seat.id
        )  # 关联 seats 表
        .join(models.Room, models.Seat.room_id == models.Room.id)  # 关联 rooms 表
        .group_by(models.Room.name)  # 按房间名称分组
        .all()
    )

    response_data = [
        {"name": response.location, "total": response.total}
        for response in reservation_stats
    ]

    return response_data


@router.post(
    "/", response_model=ReservationResponse, status_code=status.HTTP_201_CREATED
)
async def create_reservation(
    reservation: ReservationCreate,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    print("🌳 def create_reservation")
    """
    创建新预约
    """

    print(reservation)
    for k, v in reservation:
        print(k, v)

    # print(reservation)
    # for k, v in reservation:
    #     print(k, v)
    # 返回模拟新创建的预约

    # # 确保 date 是一个 Python 的 date 对象
    # reservation_date = (
    #     reservation.date
    #     if isinstance(reservation.date, datetime.date)
    #     else datetime.strptime(reservation.date, "%Y-%m-%d").date()
    # )

    # 确保 date 是一个 Python 的 date 对象
    reservation_date = (
        reservation.date
        if isinstance(reservation.date, date)
        else datetime.strptime(reservation.date, "%Y-%m-%d").date()
    )

    # 创建新的预约对象
    new_reservation = models.Reservation(
        user_id=str(current_user_id),
        seat_id=reservation.seatId,
        date=reservation_date,  # 使用转换后的 date 对象
        # time_slot_id=(
        #     f"{reservation.timeSlotId}:00-{int(reservation.timeSlotId)+1}:00"
        #     if reservation.timeSlotId.isdigit()
        #     else "09:00-10:00"
        # ),
        time_slot_id=reservation.timeSlotId,
        status="已预约",
        created_at=datetime.now(),
        updated_at=datetime.now(),
    )

    # seat = db.query(models.Seat).filter(models.Seat.id == reservation.seatId).first()
    # seat.is_available = 2
    # db.commit()
    # db.refresh(seat)

    # 保存到数据库
    db.add(new_reservation)
    db.commit()
    db.refresh(new_reservation)

    # 需要将post 的预约新添加信息提交到数据库

    st = (
        db.query(models.TimeSlot.start_time)
        .filter(models.TimeSlot.id == new_reservation.time_slot_id)
        .first()
    )

    et = (
        db.query(models.TimeSlot.end_time)
        .filter(models.TimeSlot.id == new_reservation.time_slot_id)
        .first()
    )

    seat = (
        db.query(models.Seat).filter(models.Seat.id == new_reservation.seat_id).first()
    )

    room = db.query(models.Room).filter(models.Room.id == seat.room_id).first()

    reservation_date = {
        "id": new_reservation.id,
        "seatId": str(new_reservation.seat_id),
        "seatNumber": f"{seat.seat_number}",  # 模拟座位号
        "location": f"{room.name}({room.location})",  # 模拟位置
        "userId": str(current_user_id),
        "date": new_reservation.date.strftime("%Y-%m-%d"),  # 转换为字符串
        # "timeSlot": (
        #     f"{new_reservation.time_slot_id}:00-{int(new_reservation.time_slot_id)+1}:00"
        #     if new_reservation.time_slot_id.isdigit()
        #     else "09:00-10:00"
        # ),
        "timeSlot": f"{st[0]}-{et[0]}",
        "status": new_reservation.status,
        "createdAt": datetime.fromisoformat(new_reservation.created_at.isoformat()),
        "updatedAt": datetime.fromisoformat(new_reservation.updated_at.isoformat()),
    }

    # new_reservation = {
    #     "id": "999",  # 假设这是新生成的ID
    #     "seatId": reservation.seatId,
    #     "seatNumber": f"S{reservation.seatId}",  # 模拟座位号
    #     "location": "新创建的预约位置",
    #     "userId": str(current_user_id),
    #     "date": str(reservation.date),
    #     "timeSlot": (
    #         f"{reservation.timeSlotId}:00-{int(reservation.timeSlotId)+1}:00"
    #         if reservation.timeSlotId.isdigit()
    #         else "09:00-10:00"
    #     ),
    #     "status": "已预约",
    #     "createdAt": datetime.now(),
    #     "updatedAt": datetime.now(),
    # }
    # return

    print(reservation_date)
    return reservation_date


@router.delete("/{reservation_id}", response_model=ReservationResponse)
async def cancel_reservation(
    reservation_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    取消预约
    """
    print("❌ 删除预约座位")
    print("🌳 def cancel_reservation")
    # 从数据库中查找对应的预约
    reservation = (
        db.query(models.Reservation)
        .filter(models.Reservation.id == reservation_id)
        .first()
    )

    if not reservation:
        raise HTTPException(status_code=404, detail="预约不存在")

    # 验证预约是否属于当前用户
    if str(reservation.user_id) != current_user_id:
        print("current_user_id", current_user_id, type(current_user_id))  # str
        print(
            "reservation.user_id", reservation.user_id, type(reservation.user_id)
        )  # int
        raise HTTPException(status_code=403, detail="无权操作此预约")

    # 删除预约记录
    db.delete(reservation)
    db.commit()

    st = (
        db.query(models.TimeSlot.start_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
    )

    et = (
        db.query(models.TimeSlot.end_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
    )

    # 返回已取消的预约信息
    cancelled_reservation = {
        "id": reservation.id,
        "seatId": str(reservation.seat_id),
        "seatNumber": f"S{reservation.seat_id}",  # 模拟座位号
        "location": "预约位置",  # 模拟位置
        "userId": str(reservation.user_id),
        "date": reservation.date.strftime("%Y-%m-%d"),  # 转换为字符串
        # "timeSlot": (
        #     f"{reservation.time_slot_id}:00-{int(reservation.time_slot_id)+1}:00"
        #     if reservation.time_slot_id.isdigit()
        #     else "09:00-10:00"
        # ),
        "timeSlot": f"{st[0]}-{et[0]}",
        "status": "已取消",
        "createdAt": reservation.created_at.isoformat(),
        "updatedAt": datetime.now().isoformat(),
    }

    return cancelled_reservation


@router.get("/{reservation_id}", response_model=ReservationDetailResponse)
async def get_reservation(
    reservation_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    获取预约详情
    """

    print("🌳 def get_reservation")
    print("reservation_id", reservation_id)
    # 查找对应的预约
    # reservation = next(
    #     (r for r in MOCK_RESERVATIONS if r["id"] == reservation_id), None
    # )

    # if not reservation:
    #     raise HTTPException(status_code=404, detail="预约不存在")

    # # 验证预约是否属于当前用户
    # if reservation["userId"] != str(current_user_id):
    #     raise HTTPException(status_code=403, detail="无权查看此预约")

    # 验证预约是否属于当前用户
    if str(reservation.user_id) != str(current_user_id):
        print("current_user_id", current_user_id, type(current_user_id))
        print("reservation.user_id", reservation.user_id, type(reservation.user_id))
        raise HTTPException(status_code=403, detail="无权操作此预约")

    reservation = (
        db.query(models.Reservation)
        .filter((models.Reservation.id) == str(reservation_id))
        .first()
    )

    return reservation


@router.post("/{reservation_id}/checkin", response_model=ReservationResponse)
async def checkin_reservation(
    reservation_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db),
):
    """
    签到
    """
    # 查找对应的预约
    print("🌳 def checkin_reservation")

    print("reservation_id", reservation_id)
    # reservation = next(
    #     (r for r in MOCK_RESERVATIONS if r["id"] == reservation_id), None
    # )

    # if not reservation:
    #     raise HTTPException(status_code=404, detail="预约不存在")

    # if reservation["status"] != "已预约":
    #     print("reservation_status", reservation["status"])
    #     raise HTTPException(status_code=400, detail="预约状态不允许签到")

    # 返回已签到的预约
    # checked_in_reservation = {
    #     **reservation,
    #     "status": "已签到",
    #     "checkinTime": datetime.now().isoformat(),
    #     "updatedAt": datetime.now(),
    # }
    # print("MOCKED_RESERVATIONS")
    # print(checked_in_reservation)

    # 从数据库中查找对应的预约
    reservation = (
        db.query(models.Reservation)
        .filter((models.Reservation.id) == str(reservation_id))
        .first()
    )

    print(reservation)

    if not reservation:
        raise HTTPException(status_code=404, detail="预约不存在")

    # 验证预约是否属于当前用户
    if str(reservation.user_id) != str(current_user_id):
        print("current_user_id", current_user_id, type(current_user_id))
        print("reservation.user_id", reservation.user_id, type(reservation.user_id))
        raise HTTPException(status_code=403, detail="无权操作此预约")

    # 验证预约状态是否允许签到
    if reservation.status != "已预约":
        raise HTTPException(status_code=400, detail="预约状态不允许签到")

    # 更新预约状态为 "已签到"
    reservation.status = "已签到"
    reservation.updated_at = datetime.now()

    # 提交更改到数据库
    db.commit()
    db.refresh(reservation)

    st = (
        db.query(models.TimeSlot.start_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
    )

    et = (
        db.query(models.TimeSlot.end_time)
        .filter(models.TimeSlot.id == reservation.time_slot_id)
        .first()
    )

    seat = db.query(models.Seat).filter(models.Seat.id == reservation.seat_id).first()

    room = db.query(models.Room).filter(models.Room.id == seat.room_id).first()

    # 返回已签到的预约信息
    checked_in_reservation = {
        # **reservation,
        "id": reservation.id,
        "seatId": str(reservation.seat_id),
        "seatNumber": f"{seat.seat_number}",  # 模拟座位号
        "location": f"{room.name}({room.location})",  # 模拟位置
        "userId": str(reservation.user_id),
        "date": reservation.date.strftime("%Y-%m-%d"),  # 转换为字符串
        # "timeSlot": (
        #     f"{reservation.time_slot_id}:00-{int(reservation.time_slot_id)+1}:00"
        #     if reservation.time_slot_id.isdigit()
        #     else "09:00-10:00"
        # ),
        "timeSlot": f"{st[0]}-{et[0]}",
        "status": reservation.status,
        "checkinTime": datetime.now().isoformat(),
        "createdAt": reservation.created_at.isoformat(),
        "updatedAt": reservation.updated_at.isoformat(),
    }
    # print(checked_in_reservation)
    return checked_in_reservation
