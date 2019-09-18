import time
import datetime
import sys

from activity import ActivityList, TimeEntry, Activity, save_activities, ActivityItem
from linux import get_active_window_info

if sys.platform not in ['linux', 'linux2']:
    raise Exception('Only linux platform is supported')


if __name__ == '__main__':
    active_app_name = ""
    active_window_title = ""
    start_time = datetime.datetime.now()
    activity_list = ActivityList()
    first_time = True

    try:
        while True:
            new_app_name, new_window_title = get_active_window_info()

            if active_app_name != new_app_name or active_window_title != new_window_title:
                if not first_time:
                    print(active_app_name, active_window_title)
                    time_entry = TimeEntry(start_time, datetime.datetime.now())
                    activity_item = ActivityItem(active_window_title, [time_entry])

                    for activity in activity_list.activities:
                        if activity.name == active_app_name:
                            for item in activity.items:
                                if item.title == active_window_title:
                                    item.time_entries.append(time_entry)
                                    break
                            else:
                                activity.items.append(activity_item)
                            break
                    else:
                        activity = Activity(active_app_name, [activity_item])
                        activity_list.activities.append(activity)
                    save_activities(activity_list)
                    start_time = datetime.datetime.now()
                first_time = False
                active_app_name, active_window_title = new_app_name, new_window_title
            time.sleep(1)
    except KeyboardInterrupt:
        save_activities(activity_list)
