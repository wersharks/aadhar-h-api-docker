from typing import Union

from fastapi import FastAPI
from bhuvan import BhuvanScraper
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
def read_root():
    return {"status": "working"}


@app.get("/aadhar/nearby/")
def read_item(x: str, y:str, radius: int = 5):
    b = BhuvanScraper(x, y, radius)
    return b.scrape()