import os
from dotenv import load_dotenv 


load_dotenv()

AWS_ACCESS_KEY_ID = os.getenv("AWS_ACCESS_KEY_ID")
AWS_SECRET_ACCESS_KEY = os.getenv("AWS_SECRET_ACCESS_KEY")
AWS_DEFAULT_REGION = os.getenv("AWS_DEFAULT_REGION")
S3_BUCKET_NAME = os.getenv("AWS_BUCKET")
S3_PREFIX =  "accesslog/0e254868-25ba-461f-bccb-b54efe7f90e7/"

if not all([AWS_ACCESS_KEY_ID, AWS_SECRET_ACCESS_KEY, AWS_DEFAULT_REGION]):
    raise EnvironmentError("❌ Missing AWS credentials. Check .env file.")
