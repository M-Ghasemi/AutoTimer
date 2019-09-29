import argparse
import os
import subprocess
import sys

from settings import DAEMON_DIR, DAEMON_FILE_PATH, AUTO_TIMER_FILE, DAEMON_FILE_NAME, COMMANDS

daemon_str = """
[Unit]
Description=Linux Auto Timer
After=graphical.target graphical-session.target nautilus.service

[Service]
# User={user}
# Group={group}
ExecStart={python} {auto_timer} {run_command}
Restart=always
RestartSec=3

[Install]
WantedBy=default.target
"""


def start_service():
    print('starting...')
    subprocess.run(['systemctl', '--user', 'start', DAEMON_FILE_NAME])


def stop_service():
    print('stopping...')
    subprocess.run(['systemctl', '--user', 'stop', DAEMON_FILE_NAME])


def restart_service():
    print('restarting...')
    subprocess.run(['systemctl', '--user', 'restart', DAEMON_FILE_NAME])


def enable_service():
    print('enabling...')
    subprocess.run(['systemctl', '--user', 'enable', DAEMON_FILE_NAME])


def disable_service():
    print('disabling...')
    subprocess.run(['systemctl', '--user', 'disable', DAEMON_FILE_NAME])


def status():
    subprocess.run(['systemctl', '--user', 'status', DAEMON_FILE_NAME])


def undaemonize():
    disable_service()
    stop_service()
    try:
        os.remove(DAEMON_FILE_PATH)
    except FileNotFoundError:
        pass


def daemonize():
    if os.path.isfile(DAEMON_FILE_PATH):
        print('service already created!')
        undaemonize()

    os.makedirs(DAEMON_DIR, exist_ok=True)
    try:
        with open(DAEMON_FILE_PATH, 'w') as daemon_file:
            daemon_file.write(
                daemon_str.format(
                    user=os.environ['USER'],
                    group=os.environ['USER'],
                    python=sys.executable,
                    auto_timer=AUTO_TIMER_FILE,
                    run_command=COMMANDS.RUN
                )
            )
    except Exception as e:
        print(repr(e))
    else:
        print('service created')
        print('reloading daemons')
        subprocess.run(['systemctl', '--user', 'daemon-reload'])


def run():
    DAEMONIZE = 'daemonize'
    UNDAEMONIZE = 'undaemonize'
    START = 'start'
    STOP = 'stop'
    RESTART = 'restart'
    ENABLE = 'enable'
    DISABLE = 'disable'
    STATUS = 'status'

    run_command = {
        START: start_service,
        STOP: stop_service,
        RESTART: restart_service,
        STATUS: status,
        ENABLE: enable_service,
        DISABLE: disable_service,
        DAEMONIZE: daemonize,
        UNDAEMONIZE: undaemonize,
    }
    parser = argparse.ArgumentParser()
    parser.add_argument('command', choices=[DAEMONIZE, UNDAEMONIZE, START, STOP, RESTART, ENABLE, DISABLE, STATUS],
                        help=("`daemonize`: create service, `undaemonize`: delete service, "
                              "`start`: start service, `stop`: stop service, `status`: print status, "
                              "`enable`: enable service to run at startup, "
                              "`disable`: disable service from running at startup"))

    args = parser.parse_args()
    run_command[args.command]()


if __name__ == '__main__':
    run()
