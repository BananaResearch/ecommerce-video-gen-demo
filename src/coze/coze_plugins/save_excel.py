from io import BytesIO
import os
import pandas as pd
from datetime import datetime
import oss2
from dotenv import load_dotenv, find_dotenv

load_dotenv(find_dotenv())

OSS_ACCESS_KEY_ID = os.getenv("OSS_ACCESS_KEY_ID")
OSS_ACCESS_KEY_SECRET = os.getenv("OSS_ACCESS_KEY_SECRET")
OSS_BUCKET_NAME = os.getenv("OSS_BUCKET_NAME")

def save_excel(data, filename):
    # Convert list of dicts to DataFrame if needed
    if not isinstance(data, pd.DataFrame):
        data = pd.DataFrame(data)

    # use the current month as the folder name
    month = datetime.now().strftime("%Y%m")

    # Generate the timestamp for the filename
    timestamp = datetime.now().strftime("%Y%m%d%H%M%S%f")[:-3]  # yyyymmddhhmmssmmm format
    
    # Construct the new filename
    full_filename = f"{month}/{filename}_{timestamp}.xlsx"

    # Create an in-memory bytes buffer
    excel_buffer = BytesIO()

    # Save the DataFrame to an Excel file in the buffer
    data.to_excel(excel_buffer, index=False)

    # Initialize the OSS2 authentication and bucket information
    auth = oss2.Auth(OSS_ACCESS_KEY_ID, OSS_ACCESS_KEY_SECRET)
    bucket = oss2.Bucket(auth, 'https://oss-cn-beijing.aliyuncs.com', OSS_BUCKET_NAME)

    # Move the buffer's cursor to the beginning
    excel_buffer.seek(0)

    # Upload the Excel file from the buffer to OSS
    bucket.put_object(full_filename, excel_buffer.getvalue())

    # Generate a signed URL for downloading (valid for 1 hour)
    expires_in_seconds = 3600  # 1 hour
    download_url = bucket.sign_url('GET', full_filename, expires_in_seconds)

    return download_url

if __name__ == "__main__":
    data = [{'Name': 'Alice', 'Age': 25}, {'Name': 'Bob', 'Age': 30} ]
    url = save_excel(data, "test_data")
    print("Download URL:", url)