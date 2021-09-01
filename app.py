import os

import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

# Model
import model.model1 as model1

from typing import Optional
from pydantic import BaseModel

# data base connection
import psycopg2
from config import config
from get_db_data import get_all_data, get_data
from get_coordinates import get_geojson


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


@app.get("/image/",
         responses={200: {"description": "", "content": {"image/jpeg": {"example": ""}}}})
def get_image():

    THIS_FOLDER = os.path.dirname(os.path.abspath(__file__))
    my_file = os.path.join(THIS_FOLDER, """example.jpg""")
    print(my_file)

    if os.path.exists(my_file):
        return FileResponse(my_file, media_type="image/jpeg", filename="example.jpg")
    return {"error": "File not found!",
            "path": my_file}


@app.get("/coordinates/")
async def get_all_coordinates():
    data = get_geojson()
    print(data)
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

if __name__ == "__main__":
    # Run the app with uvicorn ASGI server asyncio frameworks. That basically responds to request on parallel and faster
    uvicorn.run("app:app", port=8000, reload=True)
