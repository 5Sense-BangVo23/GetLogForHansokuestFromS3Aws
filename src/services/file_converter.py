import csv
import json
import re
import os
import datetime
from utils.logger import log_info, log_error


def get_unique_filename(base_name, extension):
    """Tạo tên file không trùng lặp bằng cách thêm số thứ tự nếu cần."""
    counter = 1
    new_filename = f"{base_name}{extension}"

    while os.path.exists(new_filename):  
        new_filename = f"{base_name}_{counter}{extension}"
        counter += 1

    return new_filename


def convert_log_txt_to_csv(txt_path, output_dir="output"):
    """Chuyển đổi file log TXT thành CSV với tên file không bị trùng."""
    try:
        os.makedirs(output_dir, exist_ok=True) 
        
        timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
        base_filename = os.path.join(output_dir, f"log_{timestamp}")
        csv_path = get_unique_filename(base_filename, ".csv")

        seen_entries = set()  

        with open(txt_path, "r", encoding="utf-8") as txt_file, open(csv_path, "w", newline="", encoding="utf-8") as csv_file:
            writer = csv.writer(csv_file)
            writer.writerow(["timestamp", "ip", "user_agent", "path", "method"])  

            for line in txt_file:
                log_entry = parse_log_line(line.strip())
                if log_entry:
                    entry_tuple = (log_entry["timestamp"], log_entry["ip"], log_entry["user_agent"], log_entry["path"], log_entry["method"])
                    
                    if entry_tuple not in seen_entries:  
                        writer.writerow(entry_tuple)
                        seen_entries.add(entry_tuple)

        log_info(f"✅ Converted LOG to CSV: {csv_path}")
        return csv_path

    except Exception as e:
        log_error(f"❌ ERROR converting {txt_path} to CSV: {e}")
        return None


def parse_log_line(log_line):
    """Phân tích một dòng log thành dictionary có cấu trúc."""
    try:
        match = re.match(r"([\d\-T:.Z]+)\s(.*)", log_line)
        if not match:
            return None

        timestamp, json_part = match.groups()
        log_data = json.loads(json_part)

        formatted_timestamp = timestamp.replace("T", " ").split(".")[0]

        return {
            "timestamp": formatted_timestamp,
            "ip": log_data.get("ip", ""),
            "user_agent": log_data.get("user_agent", ""),
            "path": log_data.get("path", ""),
            "method": log_data.get("method", "")
        }

    except (json.JSONDecodeError, IndexError) as e:
        log_error(f"❌ ERROR parsing log line: {log_line} | {e}")
        return None
