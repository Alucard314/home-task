from fastapi import FastAPI, UploadFile, File, HTTPException
from app import gcloud_utils

app = FastAPI()

@app.get("/files")
async def list_files():
    return await gcloud_utils.list_files()

@app.get("/files/{name}")
async def get_file_url(name: str):
    url = await gcloud_utils.get_signed_url(name)
    if not url:
        raise HTTPException(status_code = 404, detail = "File not found")
    return {"url": url}

@app.post("/files")
async def upload_file(file: UploadFile = File(...)):
    filename = await gcloud_utils.upload_file(file)
    return {"filename": filename}

@app.delete("/files/{name}")
async def delete_file(name: str):
    deleted_filename = await gcloud_utils.delete_file(name)
    if not deleted_filename:
        raise HTTPException(status_code = 404, detail = "File not found")
    return {"filename": deleted_filename}
















# @app.get("/users/{user_id}/details")
# def read_user_details(user_id: int, include_email:bool = False):
#     if include_email:
#         return{"user_id":user_id, "include email:" : "email included "}
#     else:
#         return{"user_id":user_id, "include email:" : "email not included "}

# @app.get("/users/")
# def read_user(user_id: int, name:str = None):
#     return {"user": user_id, "name":name}

# @app.get("/users/{user_id}")
# def read_user(user_id: int):
#     return {"user": user_id}

# @app.get("/")
# def read_root():
#     return {"message:", "Welcome to FastAPI!"}

# @app.post("/items/")
# def create_item(name: str, price:float):
#     return {"name": name, "price": price}

# @app.put("/items/{item_id}")
# def update_item(item_id: int, name: str, price: float):
#     return {"item_id": item_id, "name": name, "price": price}

# @app.delete("/items/{item_id}")
# def delete_item(item_id: int):
#     return {"message": f"Item {item_id} deleted successfully"}

