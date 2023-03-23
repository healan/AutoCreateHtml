import os
import uuid
from fastapi import FastAPI, File, UploadFile, Form
from fastapi.responses import FileResponse

app = FastAPI()


@app.get("/")
async def root():
    return {"message": "Hello World"}


@app.post("/photo")
async def uploadPhoto(image: UploadFile):
    UPLOAD_DIR = "./image"

    content = await image.read()
    filename = f"{str(uuid.uuid4())}.jpg"  # uuid로 유니크한 파일명으로 변경
    print(19, filename)

    with open(os.path.join(UPLOAD_DIR, filename), "wb") as fp:
        fp.write(content)  # 서버 로컬 스토리지에 이미지 저장 (쓰기)

    return {"filename": filename}


@app.get("/before/onephoto")
async def getPhoto(filename):
    resizeImg_path = '/NAS2/KHL/resizeImg/before/'
    return FileResponse(resizeImg_path+filename)


@app.get("/after/onephoto")
async def getPhoto(filename):
    resizeImg_path = '/NAS2/KHL/resizeImg/after/'
    return FileResponse(resizeImg_path+filename)

# @app.get("/beforeFullsize/onephoto")
# async def getPhoto(filename):
#     resizeImg_path = '/NAS2/KHL/before/'
#     return FileResponse(resizeImg_path+filename)


@app.get("/fullsize/origin/onephoto")
async def getPhoto(filename):
    resizeImg_path = '/NAS2/KHL/resizeFullImg/origin/'
    return FileResponse(resizeImg_path+filename)


@app.get("/fullsize/contour/onephoto")
async def getPhoto(filename):
    resizeImg_path = '/NAS2/KHL/resizeFullImg/contour/'
    return FileResponse(resizeImg_path+filename)


@app.get("/imagelist")
async def getImageList():
    imgList = os.listdir('./image')
    print(imgList)
    return imgList
