import time
import datetime
import sys

from linux import get_active_window_info
from settings import SAVE_TO_FILE_INTERVAL
from activity import (
    ActivityList,
    TimeEntry,
    Activity,
    ActivityItem,
    save_activities)

if sys.platform not in ['linux', 'linux2']:
    raise Exception('Only linux platform is supported')


if __name__ == '__main__':
    active_app_name = active_window_title = ""
    activity_list = ActivityList()
    start_time = datetime.datetime.now()
    last_saved_time = datetime.datetime.now()

    try:
        while True:
            new_app_name, new_window_title = get_active_window_info()

            if active_app_name != new_app_name or active_window_title != new_window_title:
                if active_app_name != "":
                    time_entry = TimeEntry(start_time, datetime.datetime.now())
                    activity_item = ActivityItem(active_window_title, [time_entry])
                    sys.stdout.write(
                        """\r{app_name} => {title}
                        \rTime (hours:minutes:seconds): {hours}:{minutes}:{seconds}
                        """.format(
                            app_name=active_app_name, title=active_window_title,
                            hours=time_entry.hours, minutes=time_entry.minutes, seconds=time_entry.seconds
                        )
                    )

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

                    if datetime.datetime.now() - last_saved_time > SAVE_TO_FILE_INTERVAL:
                        sys.stdout.write('\rSaving activities.json\n')
                        save_activities(activity_list)
                        last_saved_time = datetime.datetime.now()

                    start_time = datetime.datetime.now()
                active_app_name, active_window_title = new_app_name, new_window_title
            time.sleep(1)
    except KeyboardInterrupt as e:
        save_activities(activity_list)
        print(repr(e))
