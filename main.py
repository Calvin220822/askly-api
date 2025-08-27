from fastapi import FastAPI
from db import init_db
from routers import agents, files
from dotenv import load_dotenv

# Load environment variables from .env
load_dotenv()

app = FastAPI()

# 初始化数据库连接池
init_db()

# 挂载路由
app.include_router(agents.router, prefix="/api")
app.include_router(files.router, prefix="/api")