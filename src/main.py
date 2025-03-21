import os
from dependencies import get_s3_client
from config import S3_BUCKET_NAME, S3_PREFIX
from services.s3_service import list_all_files, download_and_extract_gz
from utils.logger import log_info, log_error
from services.file_converter import convert_log_txt_to_csv

def main():
    log_info("🚀 Starting S3 Data Processor...")

    s3 = get_s3_client()
    files = list_all_files(s3, S3_BUCKET_NAME, S3_PREFIX)

    if not files:
        log_info(f"🛑 No files found in '{S3_PREFIX}' directory.")
        return

    download_dir = "downloaded_logs"
    extract_dir = "extracted_logs"
    output_dir = "csv_logs"
    os.makedirs(output_dir, exist_ok=True)

    log_info(f"📥 Found {len(files)} files. Processing...")

    for obj in files:
        s3_key = obj["Key"]
        txt_path = download_and_extract_gz(s3, S3_BUCKET_NAME, s3_key, download_dir, extract_dir)
        
        if txt_path:
            csv_filename = os.path.basename(txt_path).replace(".txt", ".csv")
            csv_path = os.path.join(output_dir, csv_filename)
            convert_log_txt_to_csv(txt_path, csv_path)

    log_info("🎉 All files processed!")

if __name__ == "__main__":
    main()
