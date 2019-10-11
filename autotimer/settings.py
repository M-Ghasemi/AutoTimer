import datetime
import os
from collections import namedtuple


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

# you are free to change these variables
DATA_DIR = 'data'
ACTIVITIES_JSON_FILE = "activities.json"
SAVE_TO_FILE_INTERVAL = datetime.timedelta(hours=0, minutes=0, seconds=30)
DAEMON_FILE_NAME = 'auto_timer.service'

# DO NOT CHANGE UNLESS YOU KNOW WHAT YOU ARE DOING
ACTIVITIES_JSON_FILE_PATH = os.path.join(BASE_DIR, DATA_DIR, ACTIVITIES_JSON_FILE)
DAEMON_DIR = os.path.join(os.environ['HOME'], '.config', 'systemd', 'user')
DAEMON_FILE_PATH = os.path.join(DAEMON_DIR, DAEMON_FILE_NAME)

# MAKE SURE THAT DATA DIRECTORY EXISTS
os.makedirs(os.path.join(BASE_DIR, DATA_DIR), exist_ok=True)

# DO NOT CHANGE
AUTO_TIMER_FILE = os.path.join(BASE_DIR, 'timer.py')
_COMMANDS = namedtuple(
    'commands',
    ['RUN', 'HOURS_REPORT']
)
_OPTIONS = namedtuple(
    'options',
    [
        'FINE_GRAINED',
        'FULL_DETAILS',
        'TIME_COLOR',
        'TITLE_COLOR',
        'START_TIME',
        'END_TIME',
    ]
)
_COLORS = namedtuple(
    'colors',
    ['black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow']
)
COLORS = _COLORS('black', 'blue', 'cyan', 'green', 'magenta', 'red', 'white', 'yellow')
# ui
BOLD = True
NORMAL = False


# you are free to change these variables but remember to use the exact
# same string while calling timer.py
COMMANDS = _COMMANDS(
    RUN='run',
    HOURS_REPORT='hours-report'
)
OPTIONS = _OPTIONS(
    FINE_GRAINED='--fine-grained',
    FULL_DETAILS='--full-details',
    TIME_COLOR='--time-color',
    TITLE_COLOR='--title-color',
    START_TIME='--start-time',
    END_TIME='--end-time',
)
# report colors
TIME_COLOR = COLORS.cyan
TIME_FONT_THICKNESS = BOLD  # choices: [BOLD, NORMAL]
MAIN_TITLE_COLOR = COLORS.white
TITLE_COLOR = COLORS.white
APP_TITLE_COLOR = COLORS.yellow
DEFAULT_FONT_COLOR = COLORS.white

