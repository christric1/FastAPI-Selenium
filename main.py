from fastapi import FastAPI, BackgroundTasks, HTTPException
from pydantic import BaseModel
from extract import *
import os


SECRET = os.getenv("SECRET")

app = FastAPI()

class Msg(BaseModel):
    msg: str
    secret: str

@app.get("/")
async def root():
    return {"message": "Hello World. Welcome to FastAPI!"}

@app.get("/hulan")
async def demo_get(topic: str="馬哥", len: str="100"):
    driver=createDriver()

    homepage = getHulan(driver, topic, len)
    driver.close()
    return homepage

@app.get("/drawLots")
async def demo_get():
    driver=createDriver()

    homepage = drawLots(driver)
    driver.close()
    return homepage

@app.post("/backgroundDemo")
async def demo_post(inp: Msg, background_tasks: BackgroundTasks):
    
    background_tasks.add_task(doBackgroundTask, inp)
    return {"message": "Success, background task started"}