import datetime
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

SAVE_TO_FILE_INTERVAL = datetime.timedelta(hours=0, minutes=0, seconds=2)
ACTIVITIES_JSON_FILE_PATH = os.path.join(BASE_DIR, "activities.json")

DAEMON_DIR = os.path.join(os.environ['HOME'], '.config', 'systemd', 'user')
DAEMON_FILE_NAME = 'auto_timer.service'
DAEMON_FILE_PATH = os.path.join(DAEMON_DIR, DAEMON_FILE_NAME)

AUTO_TIMER_FILE = os.path.join(BASE_DIR, 'autotimer.py')
