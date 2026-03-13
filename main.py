import threading
import uvicorn
import os

from scheduler import scheduler
from api import app

def start_scheduler():
    scheduler.start()

if __name__ == "__main__":

    # start scheduler in background
    t = threading.Thread(target=start_scheduler)
    t.start()

    # get port from Render environment
    port = int(os.environ.get("PORT", 10000))

    # start API server
    uvicorn.run(app, host="0.0.0.0", port=port)
