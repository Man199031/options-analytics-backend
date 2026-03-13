from fastapi import FastAPI
import json
import os
from datetime import date

app = FastAPI()

@app.get("/api/metrics/{index}")

def get_metrics(index):

    file=f"data/{index}/{date.today()}.json"

    if not os.path.exists(file):
        return []

    with open(file) as f:
        return json.load(f)