import datetime
import os


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# you are free to change these variables
ACTIVITIES_JSON_FILE = "activities.json"
SAVE_TO_FILE_INTERVAL = datetime.timedelta(hours=0, minutes=0, seconds=30)
DAEMON_FILE_NAME = 'auto_timer.service'

# DO NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING
ACTIVITIES_JSON_FILE_PATH = os.path.join(BASE_DIR, ACTIVITIES_JSON_FILE)
DAEMON_DIR = os.path.join(os.environ['HOME'], '.config', 'systemd', 'user')
DAEMON_FILE_PATH = os.path.join(DAEMON_DIR, DAEMON_FILE_NAME)

# DO NOT CHANGE
AUTO_TIMER_FILE = os.path.join(BASE_DIR, 'autotimer.py')
