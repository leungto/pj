import fastapi
from fastapi.middleware.cors import CORSMiddleware
from contextlib import asynccontextmanager
from routes.auth import router as auth_router
from routes.rooms import router as rooms_router
from routes.seats import router as seats_router
from routes.bookings import router as bookings_router
from routes.reservations import router as reservations_router
from routes.time_slots import router as time_slots_router
from routes.users import router as users_router
from routes.admin import router as admin_router

# 导入数据库模块
from database import create_tables

@asynccontextmanager
async def lifespan(app: fastapi.FastAPI):
    # 启动时执行
    create_tables()
    yield
    # 关闭时执行
    pass

app = fastapi.FastAPI(lifespan=lifespan)

# 前端URL，根据实际情况调整
FRONTEND_URL = "http://localhost:3000"  # 假设前端运行在3000端口

# 添加CORS中间件
# 关于CORS参考：https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=[FRONTEND_URL],  # 明确指定允许的前端源
    allow_credentials=True,  # 与前端的same-origin设置匹配
    allow_methods=["GET", "POST", "PUT", "DELETE", "PATCH", "OPTIONS"],  # 明确指定允许的方法
    allow_headers=["Content-Type", "Authorization", "X-Requested-With"],  # 明确指定允许的头部
)

@app.get("/")
def read_root():
    return {"message": "Hello, World!"}

# 注册路由 (注意，这里有一个prefix)
app.include_router(auth_router, prefix="/api/auth", tags=["auth"])
app.include_router(rooms_router, prefix="/api/rooms", tags=["rooms"])
app.include_router(seats_router, prefix="/api/seats", tags=["seats"])
app.include_router(bookings_router, prefix="/api/bookings", tags=["bookings"])
app.include_router(reservations_router, prefix="/api/reservations", tags=["reservations"])
app.include_router(time_slots_router, prefix="/api/time-slots", tags=["time-slots"])
app.include_router(users_router, prefix="/api/users", tags=["users"])
app.include_router(admin_router, prefix="/api/admin", tags=["admin"])

# 添加一个特定的路由用于位置数据
# 这里我们复用rooms模块中的get_all_locations函数
app.include_router(rooms_router, prefix="/api/locations", tags=["locations"])

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=3001)