import os

import uvicorn
from fastapi import FastAPI, File, UploadFile
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from dotenv import load_dotenv
import shutil

# Model
import model.model1 as model1

from typing import Optional
from pydantic import BaseModel

# data base connection
import psycopg2
from config import config
from get_db_data import get_all_data, get_data
from get_coordinates import get_geojson, get_geojson_boundaries, get_geojson_image_boundaries


class GeographicNames(BaseModel):
    """
    A class used to represent a team member
    ...

    Attributes
    ----------
    gn_id SERIAL PRIMARY KEY,
    geographic_name VARCHAR(255),
    geometry VARCHAR(255),
    site_type VARCHAR(255),
    date_mod VARCHAR(255),
    dictionary VARCHAR(255),
    geo_database VARCHAR(255),
    google_maps VARCHAR(255),
    open_street_maps VARCHAR(255),
    aerial_photograph VARCHAR(255),
    cartographic_sheet VARCHAR(255)
    """
    gn_id: str
    geographic_name: str
    geometry: str
    site: str
    date_mod: str
    geo_database: str
    google_maps: str
    open_street_maps: str
    aerial_photograph: str
    cartographic_sheet: str


app = FastAPI(title="REST API Team 18 DSA Project")
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def get_file(img_id: str, ext: str):

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    ASSETS_FOLDER = os.path.join(THIS_FOLDER, """assets""")

    directory_list = list()
    my_file_paths = list()
    for root, dirs, files in os.walk(ASSETS_FOLDER, topdown=False):
        for name in dirs:
            my_path = os.path.join(root, name)
            directory_list.append(my_path)
            if img_id == name:
                my_files = os.listdir(my_path)
                for my_file in my_files:
                    my_file_path = os.path.join(my_path, my_file)
                    file_name, file_ext = os.path.splitext(my_file)
                    if os.path.exists(my_file_path) and ext == file_ext:
                        if ext == ".json":
                            my_file_paths.append(my_file_path)
                            
                        else:
                            print(my_file_path)
                            print(my_file)
                            return FileResponse(my_file_path, media_type="image/jpeg", filename=my_file)
                   
    my_file_paths.sort()
    print(my_file_paths)

    return my_file_paths


@app.get("/status/")
async def read_notes():
    return {"status": "ok"}


@app.get("/geographic-names/")
async def get_geographic_names():
    data = get_all_data()
    return {"status": data}


@app.get("/geographic-names/{gn_id}/")
async def get_geographic_name(gn_id: str):
    data = get_data(gn_id)
    return {"status": data}

@app.get("/image/{img_id}/",
         responses={200: {"description": "", "content": {"image/jpeg": {"example": ""}}}})
async def get_image_file(img_id: str):
    if img_id == "0":
        return FileResponse("model/img_to_process.jpeg", media_type="image/jpeg", filename="img_to_process.jpeg")
    if img_id == "logo":
        return FileResponse("sample_data/logo-igac.jpeg", media_type="image/jpeg", filename="logo-igac.jpeg")
    if len(img_id) > 4:
        return FileResponse(f"sample_data/{img_id}.png", media_type="image/jpeg", filename=f"{img_id}.png")
    return get_file(img_id, ".jpg")


# gets image boundaries


@app.get("/image-boundaries/{img_id}/")
async def get_image_boundaries(img_id: str):
    my_file = get_file(img_id, ".json")
    data = get_geojson_image_boundaries(my_file[0])

    return {'status': data}

# Model
@app.get("/empty/")
async def empty_folders():
    model1.empty_folders()
    print("Files deleted!")
    return {'status': "ok"}

@app.get("/img_corners/")
async def get_img_corners():
    corners = model1.get_image_corners()
    return corners

@app.get("/process_img/")
async def process_img():
    results = model1.run_model1()    
    return results

@app.get("/get_abspath/")
async def get_abspath():
    abs_path = os.path.abspath("model")
    return {"path": abs_path}

# get marker coordinates


@app.get("/coordinates/{coor_id}/")
async def get_all_coordinates(coor_id: str):
    if coor_id == "0":
        filename = "model/text_detected.json"
        data = get_geojson(filename)
        return {'status': data}
    my_file = get_file(coor_id, ".json")
    data = get_geojson(my_file[1])
    #print(data)

    return {'status': data}

# gets bounding box boundaries
@app.get("/boundaries/{coor_id}/")
async def get_all_boundaries(coor_id: str):
    if coor_id == "0":
        filename = "model/text_detected.json"
        data = get_geojson_boundaries(filename)
        return {'status': data}
    my_file = get_file(coor_id, ".json")    
    data = get_geojson_boundaries(my_file[1])

    return {'status': data}


if __name__ == "__main__":
    # Run the app with uvicorn ASGI server asyncio frameworks. 
    # That basically responds to request on parallel and faster
    load_dotenv()
    uvicorn.run("app:app", host="0.0.0.0", port=8000, reload=True)