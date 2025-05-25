"""
Admin routes for the seat booking system.
"""
from typing import Dict, Any
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, case
from database.connection import get_db
from auth.dependencies import get_current_user_id
from mock_data.data import MOCK_SEATS, MOCK_USERS_LIST, MOCK_CHECKIN_STATS
import database.models as models   
from datetime import date

router = APIRouter()


@router.get("/dashboard-stats", response_model=Dict[str, Any])
async def get_dashboard_stats(
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取管理员仪表盘统计数据
    """
    # 计算总座位数
    
    # total_seats = len(MOCK_SEATS)
    # 计算总座位数
    total_seats = db.query(models.Seat).count()
    # 计算总用户数
    # total_users = len(MOCK_USERS_LIST)
    total_users = db.query(models.User).count()
    # 计算今日签到率
    # 从签到统计数据中计算总体签到率
    # 获取当前日期（UTC时间）
    today = date.today()
    # 查询今日预约统计
    stats = db.query(
        func.count(models.Reservation.id).label("total_reservations"),
        func.coalesce(func.sum(
            case(
                (models.Reservation.status == "已签到", 1),
                else_=0
            )
        ), 0).label("total_checkins")
    ).filter(models.Reservation.date == today).first()
    total_reservations = stats.total_reservations if stats else 0
    total_checkins = stats.total_checkins if stats else 0
    # 计算签到率百分比
    checkin_rate = 0
    if total_reservations > 0:
        checkin_rate = round((total_checkins / total_reservations) * 100)
    return {
        "totalSeats": total_seats,
        "totalUsers": total_users,
        "todayCheckinRate": checkin_rate
    }
