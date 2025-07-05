import schedule
import time
import threading
from django.utils.timezone import now, localtime
from .models import ScraperSchedule
from accounts.utils.scraper import scrape_fbi_seeking_info

def run_scraper():
    print("🚀 Running FBI Scraper Task...")
    scrape_fbi_seeking_info()

def scheduler_loop():
    def job():
        config = ScraperSchedule.get_solo()
        now_time = localtime(now()).time()  # Convert to local time per settings.TIME_ZONE

        # Compare local times (hour and minute)
        if config.run_time.hour == now_time.hour and config.run_time.minute == now_time.minute:
            run_scraper()

    schedule.every(1).minutes.do(job)

    while True:
        schedule.run_pending()
        time.sleep(1)

def start_scheduler():
    thread = threading.Thread(target=scheduler_loop, daemon=True)
    thread.start()
