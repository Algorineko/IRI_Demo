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

# 获取2D测试数据
@app.post("/get_2D_info")
async def get_2D_info(information: dict):
    time = information['time']
    altitude_start = int(information['altitude_start'])
    altitude_stop = int(information['altitude_stop'])
    altitude_stepsize = int(information['altitude_stepsize'])
    longitude = int(information['longitude'])
    latitude = int(information['latitude'])

    arr = iri2016.IRI(time, (altitude_start, altitude_stop, altitude_stepsize), longitude, latitude)
    arr_ne = arr['ne'].to_numpy().tolist()
    arr_nOp = arr['nO+'].to_numpy().tolist()
    return {"ne": arr_ne, "nOp": arr_nOp}

# 获取3D测试数据
@app.post("/get_3D_info")
async def get_3D_info(information_3d: dict):
    try:
        time = information_3d['time']
        altitude = int(information_3d['altitude'])
        longitude_start = int(information_3d['longitude_start'])
        longitude_stop = int(information_3d['longitude_stop'])
        latitude_start = int(information_3d['latitude_start'])
        latitude_stop = int(information_3d['latitude_stop'])
        position_stepsize = int(information_3d['position_stepsize'])
        ne_data = []
        # 循环遍历经纬度范围，获取Ne数据
        for lon in range(longitude_start, longitude_stop + 1, position_stepsize):
            for lat in range(latitude_start, latitude_stop + 1, position_stepsize):
                arr = iri2016.IRI(time, (altitude, altitude+1, 1), lon, lat)
                ne_value = arr['ne'].values[0]
                # 将 Ne 浓度数据添加到数组中
                ne_data.append([lon,lat,ne_value])
        return {"neData": ne_data}
    except Exception as e:
        print("Error in get_3D_info:", str(e))
        raise
