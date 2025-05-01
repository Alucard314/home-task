from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor
import asyncio
import os


# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'axiomatic-skill-458008-j5-61eabbfa819f.json'
BUCKET_NAME = "interviu-task"

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# Helper: ruleaza functii blocking in thread separat
async def run_in_thread(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, lambda: func(*args, **kwargs))

async def list_files():
    return await run_in_thread(lambda: [blob.name for blob in bucket.list_blobs()])

async def get_signed_url(blob_name):
    blob = bucket.blob(blob_name)
    exists = await run_in_thread(blob.exists)
    if not exists:
        return None
    url = blob.generate_signed_url(version = "v4", expiration = 900, method = "GET")
    return url

async def upload_file(file):
    blob = bucket.blob(file.filename)
    await run_in_thread(blob.upload_from_file, file.file)
    return file.filename

async def delete_file(blob_name):
    blob = bucket.blob(blob_name)
    exists = await run_in_thread(blob.exists)
    if not exists:
        return None
    await run_in_thread(blob.delete)
    return blob_name