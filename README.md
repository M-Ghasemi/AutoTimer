# Linux AutoTimer

Tracking the desktop applications and time spent on each application in realtime.

This repository was originally forked from [KalleHallden AutoTimer](https://github.com/KalleHallden/AutoTimer)

## Getting Started

I suppose you have **python3.5+**, **pip3** and **git** installed on a **linux** system.
Python 2.7+ also might work correctly but only python 3.5+ has been tested. 

**Step 1**: Get a copy of project:

```$ git clone git@github.com:M-Ghasemi/AutoTimer.git```

**Step 2**: Install required packages. make sure that you are in the root directory of the project (```$ cd AutoTimer```).

```$ pip install -r requirements.txt```

**Step 3**: run the autotimer script:

```$ python3 autotimer.py```

## Settings

You can specify the time interval for storing activities in "activities.json".
You also can specify the name of the file your activities saves in. the defaults are:

`ACTIVITIES_JSON_FILE = "activities.json"`<br>
`SAVE_TO_FILE_INTERVAL = datetime.timedelta(hours=0, minutes=0, seconds=30)`

(There are some more variables you can customize. take a look at settings.py)

## Daemon

In short, a Daemon is a background process. This part explains how to make AutoTimer
a daemon.

**Create AutoTimer service (Daemonize)**:

```$ python3 service.py daemonize```

**Delete AutoTimer service (UnDaemonize)**:

```$ python3 service.py undaemonize```

**<You need to first run daemonize command, before executing the following commands>**

**Start AutoTimer service**: run AutoTimer as a background service.

```$ python3 service.py start```

**Stop AutoTimer service**:

```$ python3 service.py stop```

**Status AutoTimer service**:

```$ python3 service.py status```

**Enable AutoTimer service**: enable Autotimer service to run at startup.

```$ python3 service.py enable```

**Disable AutoTimer service**: disable Autotimer service (from running at startup).

```$ python3 service.py disable```

## TODO

- add a reporter function that summarizes hours spent on each application and each window.
- add a reporter function that compares hours spent on each application and each window.
- add a reporter function that shows spent hours by percentage.
- add a some charts.