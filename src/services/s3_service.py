import os
import gzip
import shutil
from botocore.exceptions import BotoCoreError, ClientError
from utils.logger import log_info, log_error


def get_unique_filename(directory, filename):
    """Tạo tên file không trùng bằng cách thêm số thứ tự."""
    base, ext = os.path.splitext(filename)
    unique_filename = filename
    counter = 1

    while os.path.exists(os.path.join(directory, unique_filename)):
        unique_filename = f"{base}_{counter}{ext}"
        counter += 1

    return os.path.join(directory, unique_filename)


def list_all_files(s3, bucket, prefix):
    """Lấy danh sách tất cả file trong folder S3 (hỗ trợ phân trang)."""
    files = []
    continuation_token = None

    try:
        while True:
            list_kwargs = {'Bucket': bucket, 'Prefix': prefix}
            if continuation_token:
                list_kwargs['ContinuationToken'] = continuation_token

            response = s3.list_objects_v2(**list_kwargs)

            if "Contents" in response:
                files.extend(response["Contents"])

            continuation_token = response.get("NextContinuationToken")
            if not continuation_token:
                break

        return files

    except (BotoCoreError, ClientError) as e:
        log_error(f"❌ AWS S3 error: {e}")
        return []


def download_and_extract_gz(s3, bucket, s3_key, download_dir="downloads", extract_dir="extracted"):
    """Tải file từ S3, tránh trùng tên, và giải nén GZ thành TXT."""
    os.makedirs(download_dir, exist_ok=True)
    os.makedirs(extract_dir, exist_ok=True)

    gz_filename = os.path.basename(s3_key)
    gz_path = get_unique_filename(download_dir, gz_filename)  

    txt_filename = gz_filename.replace(".gz", ".txt")
    txt_path = get_unique_filename(extract_dir, txt_filename) 

    try:
        log_info(f"⬇ Downloading {s3_key} → {gz_path}")
        s3.download_file(bucket, s3_key, gz_path)
        log_info(f"✅ Downloaded: {gz_path}")

        with gzip.open(gz_path, 'rb') as gz_file, open(txt_path, 'wb') as txt_file:
            shutil.copyfileobj(gz_file, txt_file)

        log_info(f"📂 Extracted: {txt_path}")
        return txt_path

    except (BotoCoreError, ClientError, IOError) as e:
        log_error(f"❌ ERROR processing {s3_key}: {e}")
        return None
