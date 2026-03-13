import threading
import uvicorn
from scheduler import scheduler
from api import app

def start_scheduler():
    scheduler.start()

if __name__ == "__main__":

    # start background scheduler
    t = threading.Thread(target=start_scheduler)
    t.start()

    # start API server
    uvicorn.run(app, host="0.0.0.0", port=10000)