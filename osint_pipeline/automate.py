import schedule, time
from main import run_pipeline

run_pipeline()  # Initial run

schedule.every(1).hours.do(run_pipeline)
print("OSINT pipeline scheduler started, running every hour.")
print("Press Ctrl+C to exit.")
while True:
    schedule.run_pending()
    time.sleep(60)
    print("Scheduler: waiting for next run...")