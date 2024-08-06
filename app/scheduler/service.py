from apscheduler.triggers.interval import IntervalTrigger
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.executors.pool import ThreadPoolExecutor, ProcessPoolExecutor
from app.scheduler.proccess_aippt import proccess_aippt
from apscheduler.schedulers.asyncio import AsyncIOScheduler


scheduler = AsyncIOScheduler()

def init_scheduler():
    scheduler.add_job(proccess_aippt, IntervalTrigger(seconds=20))
