from apscheduler.schedulers.blocking import BlockingScheduler
from collector import process_index

indices=["NIFTY","BANKNIFTY"]

def job():

    for i in indices:
        process_index(i)

scheduler=BlockingScheduler()

scheduler.add_job(job,"interval",seconds=10)

scheduler.start()