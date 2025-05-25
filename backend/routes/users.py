"""
User routes for the seat booking system.
"""
from typing import List, Optional
from datetime import datetime
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from pydantic import BaseModel, EmailStr

from database.connection import get_db
from auth.dependencies import get_current_user_id
from mock_data.data import MOCK_USERS_LIST
from database.connection import get_db
import database.models as models   
from sqlalchemy.orm import Session

router = APIRouter()


class UserUpdateRequest(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    
    
class UserPasswordChangeRequest(BaseModel):
    currentPassword: str
    newPassword: str
    confirmPassword: str


class UserStatusUpdateRequest(BaseModel):
    status: str  # "active" | "inactive" | "banned"


class UserRoleUpdateRequest(BaseModel):
    role: str  # "user" | "admin"

def structure_user_data(user):
    return {
        "id": str(user.id),
        "name": user.name,
        "email": user.email,
        "role": user.role,
        "status": "active" if user.is_active == 1 else "inactive",
        "is_active": user.is_active,
        "is_admin": user.is_admin,
        "hashed_password" : user.hashed_password,
        "createdAt": user.created_at.isoformat(),
        "updatedAt": user.updated_at.isoformat()
    }

@router.get("/", response_model=List[dict])
async def get_all_users(
    q: Optional[str] = Query(None, description="搜索用户名或邮箱"), 
    role: Optional[str] = Query(None, description="按角色过滤"),
    status: Optional[str] = Query(None, description="按状态过滤"),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    # 从数据库获取所有用户（ORM 对象）
    users = db.query(models.User).all()
    # print(users[0].__dict__)
    # 转换为字典列表
    # print(type(users[0].is_active))
    print(users[0].is_active)
    user_list = [
        structure_user_data(user)
        for user in users
    ]
    
    # 按角色过滤
    if role:
        user_list = [u for u in user_list if u["role"] == role]
    
    # 按状态过滤
    if status:
        user_list = [u for u in user_list if u["status"] == status]
    
    # 搜索用户名或邮箱
    if q:
        user_list = [
            u for u in user_list 
            if q.lower() in u["name"].lower() or q.lower() in u["email"].lower()
        ]
    
    return user_list


@router.get("/{user_id}", response_model=dict)
async def get_user(
    user_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    获取特定用户信息
    当前用户只能查看自己的信息，管理员可以查看任何用户
    """
    # 在实际应用中，检查当前用户是否有权限查看此用户
    # 在模拟环境中，我们直接返回用户信息
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    return structure_user_data(user)


@router.put("/{user_id}", response_model=dict)
async def update_user(
    user_id: str,
    data: UserUpdateRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    更新用户信息
    当前用户只能更新自己的信息，管理员可以更新任何用户
    """
    # 在实际应用中，检查当前用户是否有权限更新此用户
    # 在模拟环境中，我们直接更新并返回用户信息
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 更新用户信息
    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email
    user.updatedAt = datetime.now().isoformat()
    db.commit()
    db.refresh(user)
    
    return structure_user_data(user)


@router.patch("/{user_id}/status", response_model=dict)
async def update_user_status(
    user_id: str,
    data: UserStatusUpdateRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    更新用户状态（管理员权限）
    """
    # 在实际应用中，检查当前用户是否为管理员
    # 在模拟环境中，我们直接更新并返回用户状态
    user = db.query(models.User).filter(models.User.id == user_id).first()
    # user = next((u for u in user_list if u.id == user_id), None)
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查状态值是否有效
    valid_statuses = ["inactive", "active","banned"]
    if data.status not in valid_statuses:
        raise HTTPException(status_code=400, detail=f"无效的状态值，有效值为: {', '.join(valid_statuses)}")
    
    # 更新用户状态
    # print(data.status)
    user.is_active = 1 if data.status == "active" else 0
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    return structure_user_data(user)


@router.patch("/{user_id}/role", response_model=dict)
async def update_user_role(
    user_id: str,
    data: UserRoleUpdateRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    更新用户角色（管理员权限）
    """
    # 在实际应用中，检查当前用户是否为管理员
    # 在模拟环境中，我们直接更新并返回用户角色
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    
    # 检查角色值是否有效
    valid_roles = ["user", "admin"]
    if user.role not in valid_roles:
        raise HTTPException(status_code=400, detail=f"无效的角色值，有效值为: {', '.join(valid_roles)}")
    
    # 更新用户角色
    user.role = "user" if data.role == "user" else "admin"
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    
    return structure_user_data(user)


@router.post("/{user_id}/change-password", response_model=dict)
async def change_password(
    user_id: str,
    data: UserPasswordChangeRequest,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    修改用户密码
    """
    # 在实际应用中，需要验证当前密码是否正确
    # 在模拟环境中，我们直接返回成功响应
    
    if data.newPassword != data.confirmPassword:
        raise HTTPException(status_code=400, detail="新密码与确认密码不匹配")
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    user.hashed_password = data.newPassword
    user.updated_at = datetime.now()
    db.commit()
    db.refresh(user)
    return {
        "message": "密码修改成功",
        "success": True
    }


@router.get("/search", response_model=List[dict])
async def search_users(
    q: str = Query(..., description="搜索关键字"),
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    搜索用户
    """
    # 在实际应用中，检查当前用户是否为管理员
    # 在模拟环境中，我们直接返回搜索结果
    
    if not q:
        return []
    user_list = db.query(models.User).all()
    # 搜索用户名或邮箱
    results = [
        u for u in user_list 
        if q.lower() in u.name.lower() or q.lower() in u.email.lower()
    ]
    
    return results



@router.delete("/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_user(
    user_id: str,
    current_user_id: int = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    """
    删除用户（管理员权限）
    """
    # 在实际应用中，检查当前用户是否为管理员
    current_user = db.query(models.User).get(current_user_id)
    if not current_user or current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="操作需要管理员权限"
        )
    # 在模拟环境中，我们直接返回成功状态
    user = db.query(models.User).filter(models.User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=404, detail="用户不存在")
    db.delete(user)
    db.commit()
    # db.refresh(user) 
    # 在实际应用中，这里会从数据库中删除或禁用用户
    return None 