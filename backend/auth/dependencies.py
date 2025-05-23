"""
Authentication dependencies for the seat booking system.
"""
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
import jwt
from settings import settings

# fastapi的依赖注入机制，会自动从请求头中获取token，并调用这个函数
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


async def get_current_user_id(token: str = Depends(oauth2_scheme)) -> int:
    """
    获取当前用户ID
    
    Args:
        token: JWT令牌
        
    Returns:
        用户ID
        
    Raises:
        HTTPException: 如果令牌无效或已过期
    """
    try:
        # 解码并验证JWT令牌
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        user_id: int = payload.get("sub")
        if user_id is None:
            raise ValueError("Invalid token payload")
        return user_id
    except jwt.ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token has expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except (jwt.InvalidTokenError, jwt.DecodeError, ValueError):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
