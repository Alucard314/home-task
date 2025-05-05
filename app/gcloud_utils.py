from google.cloud import storage
from concurrent.futures import ThreadPoolExecutor
import asyncio
import os

# Scrie key-ul din Secret Manager intr-un fisier temporar local, necesar pentru autentificarea GCS
key_content = os.getenv("SERVICE_ACCOUNT_KEY_JSON")
if key_content:
    key_path = "/tmp/key.json"
    with open(key_path, "w") as f:
        f.write(key_content)
    os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = key_path

# os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'axiomatic-skill-458008-j5-61eabbfa819f.json'

# Bucket-ul folosit
BUCKET_NAME = "interviu-task"

storage_client = storage.Client()
bucket = storage_client.bucket(BUCKET_NAME)

# Helper: ruleaza o functie blocanta (sincrona) intr-un thread separat,
# pentru a nu bloca event loop-ul aplicatie asincrone
async def run_in_thread(func, *args, **kwargs):
    loop = asyncio.get_running_loop()
    with ThreadPoolExecutor() as pool:
        return await loop.run_in_executor(pool, lambda: func(*args, **kwargs))
    


# returneasa lista tuturor fisierelor din bucket
async def list_files():
    return await run_in_thread(lambda: [blob.name for blob in bucket.list_blobs()])

# generereaza URL semnat (valid 15 minute) pentru acces la un fisier specific
async def get_signed_url(blob_name):
    blob = bucket.blob(blob_name)
    exists = await run_in_thread(blob.exists)
    if not exists:
        return None
    url = blob.generate_signed_url(version = "v4", expiration = 900, method = "GET")
    return url

# Incarca fisier in bucket dintr-un obiect 'UploadFile' primit de la FastApi
async def upload_file(file):
    blob = bucket.blob(file.filename)
    await run_in_thread(blob.upload_from_file, file.file)
    return file.filename

# Sterge un fisier dupa nume
async def delete_file(blob_name):
    blob = bucket.blob(blob_name)
    exists = await run_in_thread(blob.exists)
    if not exists:
        return None
    await run_in_thread(blob.delete)
    return blob_name

# Redenumeste un fisier (copie si sterge originalul)
async def rename_file(old_name, new_name):
    old_blob = bucket.blob(old_name)
    new_blob = bucket.blob(new_name)

    exists = await run_in_thread(old_blob.exists)
    if not exists:
        return None
    
    await run_in_thread(bucket.copy_blob, old_blob, bucket, new_name)
    await run_in_thread(old_blob.delete)

    return new_name