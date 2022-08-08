from typing import Union

from fastapi import FastAPI
from bhuvan import BhuvanScraper
app = FastAPI()


@app.get("/")
def read_root():
    return {"status": "working"}


@app.get("/aadhar/nearby/")
def read_item(x: str, y:str, radius: int = 5):
    b = BhuvanScraper(x, y, radius)
    return b.scrape()