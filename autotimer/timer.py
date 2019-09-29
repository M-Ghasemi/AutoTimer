import datetime
import sys
import time
import click

import settings

from activity import (
    ActivityList,
    TimeEntry,
    Activity,
    ActivityItem,
    save_activities)
from linux import get_active_window_info
from report import print_hours_report

if sys.platform not in ['linux', 'linux2']:
    raise Exception('Only linux platform is supported')


@click.group()
def auto_timer():
    pass


@auto_timer.command(name=settings.COMMANDS.RUN)
def start():
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

                    if datetime.datetime.now() - last_saved_time > settings.SAVE_TO_FILE_INTERVAL:
                        sys.stdout.write('\rSaving activities.json\n')
                        save_activities(activity_list)
                        last_saved_time = datetime.datetime.now()

                    start_time = datetime.datetime.now()
                active_app_name, active_window_title = new_app_name, new_window_title
            time.sleep(1)
    except KeyboardInterrupt as e:
        save_activities(activity_list)
        print(repr(e))


@auto_timer.command(name=settings.COMMANDS.HOURS_REPORT)
@click.option(settings.OPTIONS.FINE_GRAINED, default=True,
              show_default=True, type=click.BOOL,
              help='print hours spent on each application and each window/tab.')
@click.option(settings.OPTIONS.FULL_DETAILS, default=False,
              show_default=True, type=click.BOOL,
              help='Print in most details available.')
@click.option(settings.OPTIONS.TIME_COLOR, type=click.Choice(settings.COLORS),
              default=settings.TIME_COLOR, show_default=True,
              help='Times font color.')
@click.option(settings.OPTIONS.TITLE_COLOR, type=click.Choice(settings.COLORS),
              default=settings.TITLE_COLOR, show_default=True,
              help='Titles font color.')
def hours_report(fine_grained: bool, full_details: bool, time_color: str, title_color: str):
    print_hours_report(fine_grained, full_details, time_color, title_color)


if __name__ == '__main__':
    auto_timer()