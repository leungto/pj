import fastapi
from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr
import jwt
from datetime import datetime, timedelta, timezone

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


# JWT settings
# 了解JWT：https://www.ruanyifeng.com/blog/2018/07/json_web_token-tutorial.html
# JWT是最佳实践
# 但是为什么要用JWT不是因为这点，单纯因为cookies的话还得在数据库里存一个字段，但不用这两个的话，我不太清楚怎么持久化用户状态......

from settings import settings
from mock_data.data import MOCK_USERS

def create_access_token(data: dict, expires_delta: timedelta = None):
    to_encode = data.copy()
    expire = datetime.now(timezone.utc) + (expires_delta or timedelta(minutes=15))
    to_encode.update({"exp": expire.timestamp()})
    encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
    return encoded_jwt


class LoginRequest(BaseModel):
    email: str
    password: str


class RegisterRequest(BaseModel):
    name: str
    email: EmailStr
    password: str
    confirmPassword: str


@router.post("/login")
async def login(request_data: LoginRequest):
    # 实际上"必须"hash用户的密码，任何情况下都不要明文存储密码
    # 你们看看要不要hash，我懒得改了

    # Validate input
    if not request_data.email or not request_data.password:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1001, "message": "邮箱或密码不能为空"}
        )
    
    # Check if user exists and password is correct
    user = MOCK_USERS.get(request_data.email)
    if not user or user["password"] != request_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 1002, "message": "邮箱或密码错误"}
        )
    
    # Return successful response
    return {
        "user": {
            "id": user["id"],
            "name": user["name"],
            "email": user["email"],
            "role": user["role"]
        },
        "token": create_access_token(
            data={"sub": user["id"], "role": user["role"]},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    }


@router.post("/register")
async def register(request_data: RegisterRequest):
    # 验证输入
    if not request_data.email or not request_data.password or not request_data.name:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1001, "message": "所有字段都必须填写"}
        )
    
    # 验证密码确认
    if request_data.password != request_data.confirmPassword:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail={"code": 1003, "message": "密码和确认密码不匹配"}
        )
    
    # 检查邮箱是否已存在
    if request_data.email in MOCK_USERS:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail={"code": 1004, "message": "该邮箱已被注册"}
        )
    
    # 创建新用户 (在实际应用中，应该保存到数据库)
    # 为简化示例，这里只在内存中模拟
    new_user_id = str(len(MOCK_USERS) + 1)
    new_user = {
        "id": new_user_id,
        "name": request_data.name,
        "email": request_data.email,
        "password": request_data.password,  # 实际应用中应当哈希
        "role": "user"
    }
    
    # 在实际应用中，这里会将新用户保存到数据库
    # 在这个模拟示例中，我们将其添加到mock_users字典
    MOCK_USERS[request_data.email] = new_user
    
    # 返回新用户信息和令牌
    return {
        "user": {
            "id": new_user["id"],
            "name": new_user["name"],
            "email": new_user["email"],
            "role": new_user["role"]
        },
        "token": create_access_token(
            data={"sub": new_user_id, "role": new_user["role"]},
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
    }


@router.get("/me")
async def get_current_user(token: str = Depends(oauth2_scheme)):
    try:
        # 解码并验证 JWT token
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM])
        user_id = payload.get("sub")
        if not user_id:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 2001, "message": "无效的认证令牌"}
            )
            
        # 检查 token 是否过期
        exp = payload.get("exp")
        if not exp or datetime.fromtimestamp(exp, timezone.utc) < datetime.now(timezone.utc):
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail={"code": 2002, "message": "认证令牌已过期"}
            )
            
    except jwt.InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail={"code": 2001, "message": "无效的认证令牌"}
        )
    
    # 在实际应用中，这里会根据用户ID从数据库获取用户信息
    # 在这个模拟示例中，我们返回固定的用户信息
    for user in MOCK_USERS.values():
        if user["id"] == user_id:
            return {
                "id": user["id"],
                "name": user["name"],
                "email": user["email"],
                "role": user["role"]
            }
    
    # 如果找不到用户，返回默认用户
    return {
        "id": "1",
        "name": "张三",
        "email": "user@example.com",
        "role": "user"
    }