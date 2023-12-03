import os
import sys
root_path = os.getcwd()
sys.path.append(root_path)
import iri2016
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
app = FastAPI()
origins = [
    "http://localhost",
    "http://localhost:8080",  # Vue应用运行的地址
]
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # 允许所有源
    allow_credentials=True,
    allow_methods=["*"],  # 允许所有方法
    allow_headers=["*"],  # 允许所有头
)

@app.get("/")
async def root():
    return {"message": "Hello IRI"}

# 获取测试数据
@app.post("/test_ne")
async def test_ne(information: dict):
    time = information['time']
    altitude_start = int(information['artitude_start'])
    altitude_stop = int(information['artitude_stop'])
    altitude_stepsize = int(information['artitude_stepsize'])
    longitude = int(information['longitude'])
    latitude = int(information['latitude'])

    arr = iri2016.IRI(time, (altitude_start, altitude_stop, altitude_stepsize), longitude, latitude)
    arr_ne = arr['ne'].to_numpy().tolist()
    arr_nOp = arr['nO+'].to_numpy().tolist()
    return {"ne": arr_ne, "nOp": arr_nOp}
