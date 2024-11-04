import os
import json
from pathlib import Path
from datetime import datetime


def init_printer_directory():
    # 获取用户主目录
    user_home = str(Path.home())
    printer_dir = os.path.join(user_home, "Perfume_Printer")

    # 创建 .Perfume_Printer 目录（如果不存在）
    if not os.path.exists(printer_dir):
        os.makedirs(printer_dir)

    # 处理 order.json 文件
    order_file = os.path.join(printer_dir, "order.json")
    if os.path.exists(order_file):
        # 如果文件存在，用时间戳重命名
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        new_name = f"order_{timestamp}.json"
        os.rename(order_file, os.path.join(printer_dir, new_name))

    # 创建新的 order.json 文件
    with open(order_file, "w", encoding="utf-8") as f:
        json.dump([], f)

    return printer_dir
