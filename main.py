from fastapi import FastAPI, Query
import os
import json
import threading
from mock_printer import mock_printer

from utils.file_manager import init_printer_directory
from contextlib import asynccontextmanager
from models.print import PrintStatus, PrintRequest, PrintResponse, PrintStatusResponse


@asynccontextmanager
async def lifespan(app: FastAPI):
    # 启动时运行
    global printer_dir
    printer_dir = init_printer_directory()
    printer_thread = threading.Thread(
        target=mock_printer,
        args=(printer_dir,),
        daemon=True
    )
    printer_thread.start()
    print("Mock printer service started in background")
    
    yield
    
    # 关闭时运行（因为是守护线程，不需要显式关闭）
    print("Shutting down mock printer service...")


app = FastAPI(lifespan=lifespan)


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
