import json
import os
from datetime import date

def save_snapshot(index, data):

    folder = f"data/{index}"
    os.makedirs(folder, exist_ok=True)

    file = f"{folder}/{date.today()}.json"

    if os.path.exists(file):
        with open(file,"r") as f:
            records=json.load(f)
    else:
        records=[]

    records.append(data)

    with open(file,"w") as f:
        json.dump(records,f)