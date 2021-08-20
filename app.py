import uvicorn
from fastapi import FastAPI
from fastapi.middleware.wsgi import WSGIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from typing import Optional
from pydantic import BaseModel
from connect import connect

class TeamMembers(BaseModel):
    """
    A class used to represent a team member
    ...

    Attributes
    ----------
    Name : string
    email : int
    """
    name: str
    email: str
    
app = FastAPI(title = "REST API Team 18 DSA Project")
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

if __name__ == "__main__":
    # Run the app with uvicorn ASGI server asyncio frameworks. That basically responds to request on parallel and faster
    uvicorn.run("app:app", port=8000, reload=True)