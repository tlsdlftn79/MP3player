from fastapi import FastAPI, UploadFile, File, Request  # Request 추가
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from typing import List
import os

app = FastAPI()

# Static Files (MP3) 위치 설정
app.mount("/static", StaticFiles(directory="static"), name="static")

templates = Jinja2Templates(directory="templates")

# 홈페이지 설정
@app.get("/", response_class=HTMLResponse)
def read_root(request: Request):
    mp3_list = os.listdir("static/mp3")
    return templates.TemplateResponse("index.html", {"request": request, "mp3_list": mp3_list})

# MP3 파일 목록
@app.get("/mp3_list")
def mp3_list():
    files = os.listdir("static/mp3")
    return {"mp3_list": files}

# MP3 파일 업로드
@app.post("/upload_mp3/")
async def upload_mp3(mp3: UploadFile = File(...)):
    file_location = f"static/mp3/{mp3.filename}"
    with open(file_location, "wb+") as file_object:
        file_object.write(mp3.file.read())
    return {"info": f"{mp3.filename} uploaded successfully"}

# MP3 파일 다운로드 (재생은 클라이언트에서 처리)
@app.get("/download_mp3/{mp3_name}")
async def download_mp3(mp3_name: str):
    return FileResponse(path=f"static/mp3/{mp3_name}", filename=mp3_name)
