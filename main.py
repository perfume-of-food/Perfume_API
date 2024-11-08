from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
import os
import json
import threading

from utils.file_manager import init_printer_directory
from contextlib import asynccontextmanager
from models.print import PrintStatus, PrintRequest, PrintResponse, PrintStatusResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时运行
    global printer_dir
    printer_dir = init_printer_directory()
    
    yield
    
    # 关闭时运行（因为是守护线程，不需要显式关闭）
    print("Shutting down mock printer service...")


app = FastAPI(lifespan=lifespan)

# 添加 CORS 中间件配置
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源，生产环境建议设置具体的源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有请求头
)


@app.post("/print", response_model=PrintResponse)
def start_print(request: PrintRequest):
    # 将请求保存到 order.json
    order_file = os.path.join(printer_dir, "order.json")

    # 读取现有数据
    if os.path.exists(order_file):
        with open(order_file, "r", encoding="utf-8") as f:
            orders = json.load(f)
    else:
        orders = []

    # 添加新订单
    orders.append(request.model_dump())

    # 保存更新后的数据
    with open(order_file, "w", encoding="utf-8") as f:
        json.dump(orders, f, ensure_ascii=False, indent=2)

    return PrintResponse(message="Print task started", task_id=request.task_id)


@app.get("/print", response_model=PrintStatusResponse)
def get_print_status(task_id: int = Query(gt=0)):
    # 读取 status.json 文件
    status_file = os.path.join(printer_dir, "status.json")
    
    if os.path.exists(status_file):
        with open(status_file, "r", encoding="utf-8") as f:
            status_data = json.load(f)
            
        # 查找对应 task_id 的状态
        for status_entry in status_data:

            if status_entry.get("task_id") == task_id:
                return PrintStatusResponse(
                    task_id=task_id,
                    status=PrintStatus(status_entry.get("status"))
                )
    
    # 如果没有找到对应的状态，返回 NOT_FOUND
    return PrintStatusResponse(task_id=task_id, status=PrintStatus.NOT_FOUND)
