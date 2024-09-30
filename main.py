from website import create_app #website is a python package -> I can import it
from website.populate_db import update_database
from flask_apscheduler import APScheduler
from apscheduler.schedulers.background import BackgroundScheduler
import os

app = create_app()
scheduler = APScheduler(scheduler=BackgroundScheduler())

if not scheduler.running:
    scheduler.init_app(app)
    scheduler.start()

if not scheduler.get_job('update_db'):
    scheduler.add_job(
        id='update_db',
        func=lambda: update_database(app),
        trigger='cron',
        day_of_week='mon',
        hour=3,
        minute=0,
        max_instances=1
    )
        
if __name__ == '__main__':
    app.run(debug=True,use_reloader=False)

