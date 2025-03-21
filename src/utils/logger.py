import datetime

def log_info(message):
    """Ghi log thông tin."""
    print(f"[{datetime.datetime.now()}] INFO: {message}")

def log_error(message):
    """Ghi log lỗi."""
    print(f"[{datetime.datetime.now()}] ERROR: {message}")
