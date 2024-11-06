import json
import time
import os

def mock_printer(printer_dir: str):
    def ensure_status_file():
        # 确保 status.json 存在
        status_file = os.path.join(printer_dir, 'status.json')
        if not os.path.exists(status_file):
            with open(status_file, 'w') as f:
                json.dump([], f)
        return status_file

    # 初始化时确保文件存在
    ensure_status_file()

    while True:
        try:
            # 读取订单和状态，使用完整路径
            order_file = os.path.join(printer_dir, 'order.json')
            status_file = ensure_status_file()  # 读取前确保文件存在
            
            # 读取订单和状态
            with open(order_file, 'r') as f:
                orders = json.load(f)
            with open(status_file, 'r') as f:
                status_list = json.load(f)
            
            # 找到最新订单
            if orders:
                latest_task = max(orders, key=lambda x: x['task_id'])
                latest_task_id = latest_task['task_id']
                
                # 如果是新任务，添加到状态列表
                if not any(s['task_id'] == latest_task_id for s in status_list):
                    status_list.append({
                        'task_id': latest_task_id,
                        'status': 'PRINTING',
                        'task_start': time.time()  # 记录开始时间
                    })
            
            # 更新超过5秒的任务状态
            current_time = time.time()
            for task in status_list:
                if task['status'] == 'PRINTING' and current_time - task['task_start'] > 5:
                    task['status'] = 'COMPLETED'
            
            # 保存状态前再次确保文件存在
            status_file = ensure_status_file()
            with open(status_file, 'w') as f:
                json.dump(status_list, f, indent=2)
                
            time.sleep(1)
            
        except Exception as e:
            print(f"Error: {e}")
            time.sleep(1)

if __name__ == "__main__":
    print("Mock printer started...")
    mock_printer() 