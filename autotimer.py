import time
import datetime
import sys

from activity import ActivityList, TimeEntry, Activity, save_activities
from linux import get_active_window_info

if sys.platform not in ['linux', 'linux2']:
    raise Exception('Only linux platform is supported')


if __name__ == '__main__':
    active_window_name = ""
    start_time = datetime.datetime.now()
    activity_list = ActivityList()
    first_time = True

    try:
        while True:
            new_window_name = get_active_window_info()

            if active_window_name != new_window_name:
                print(active_window_name)

                if not first_time:
                    time_entry = TimeEntry(start_time, datetime.datetime.now())

                    for activity in activity_list.activities:
                        if activity.name == active_window_name:
                            activity_exists = True
                            activity.time_entries.append(time_entry)
                            break
                    else:
                        activity_exists = False

                    if not activity_exists:
                        activity = Activity(active_window_name, [time_entry])
                        activity_list.activities.append(activity)
                    save_activities(activity_list)
                    start_time = datetime.datetime.now()
                first_time = False
                active_window_name = new_window_name
            time.sleep(1)
    except KeyboardInterrupt:
        save_activities(activity_list)
