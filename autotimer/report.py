import datetime
from typing import Union

from clint.textui import colored

import settings
from activity import ActivityList, ActivityItem

spent_time_report = """The time spent on each application and each window."""


def add_to_report(report: str, text: str, indent=""):
    return "{report}\n{indent}{text}".format(indent=indent, report=report, text=text)


def format_hours(name: str,
                 time: Union[str, datetime.timedelta],
                 time_first=True,
                 time_color: str = settings.TIME_COLOR,
                 time_font_bold: bool = settings.TIME_FONT_THICKNESS,
                 name_color: str = '',
                 name_font_bold: bool = False) -> str:
    time = getattr(colored, time_color, getattr(colored, settings.TIME_COLOR))(time, bold=time_font_bold)
    if name_color or name_font_bold:
        name = getattr(colored, name_color, getattr(colored, settings.DEFAULT_FONT_COLOR)
                       )(name, bold=name_font_bold)

    if time_first:
        return "{}: {}".format(time, name)
    return "{}: {}".format(name, time)


def add_time_entries_to_report(report: str, item: ActivityItem, indent: str,
                               from_: datetime.datetime, to_: datetime.datetime):
    for time_entry in item.time_entries:
        if time_entry.time_spent_in(from_, to_).total_seconds() < 1:
            continue
        report = add_to_report(
            report,
            (time_entry.start_time.strftime("%Y-%m-%d -> from %H:%M:%S ") +
             time_entry.end_time.strftime("to %H:%M:%S")),
            indent)
    return report


def hours_report(activity_list: ActivityList,
                 from_: datetime.datetime = None, to_: datetime.datetime = None,
                 fine_grained: bool = True, full_detail=False,
                 time_color: str = '', title_color: str = '') -> str:
    """If fine_grained is True, the time spent on each window/tab will be included in addition
    to the overall time spent on each application.
    If full_detail is True the exact time spent on each window/tab also will be included."""
    report = getattr(colored, title_color or settings.MAIN_TITLE_COLOR)(spent_time_report, bold=True)
    activity_indent = "\n\r"
    item_indent = "    "
    time_interval = from_ or to_

    total_hours = format_hours(
        'Total time spent:',
        activity_list.time_spent_in(from_, to_) if time_interval else activity_list.time_spent,
        time_first=False,
        time_color=time_color,
        name_color=title_color,
        name_font_bold=True
    )
    report = add_to_report(report, total_hours, activity_indent)

    for activity in activity_list.activities:
        activity_time_spent = (
            activity.time_spent_in(from_, to_) if time_interval
            else activity.time_spent
        )  # type: datetime.timedelta

        if activity_time_spent.total_seconds() < 1:
            continue

        report = add_to_report(report, getattr(colored, title_color)(activity.name, bold=True), '\n')
        activity_hours = format_hours(
            'Total time spent',
            activity_time_spent,
            time_first=False,
            time_color=time_color, name_color=title_color, name_font_bold=True)
        report = add_to_report(report, activity_hours, item_indent)

        if fine_grained:
            for item in activity.items:
                item_time_spent = (item.time_spent_in(from_, to_) if time_interval
                                   else item.time_spent)  # type: datetime.timedelta

                if item_time_spent.total_seconds() < 1:
                    continue

                item_hours = format_hours(item.title, item_time_spent, time_color=time_color)
                report = add_to_report(report, item_hours, item_indent)
                if full_detail:
                    report = add_time_entries_to_report(report, item, item_indent * 2, from_, to_)

    return report


def print_hours_report(start_time: datetime.datetime, end_time: datetime.datetime,
                       fine_grained: bool = True, full_detail=False,
                       time_color: str = '', title_color: str = ''):
    print(hours_report(ActivityList(), start_time, end_time, fine_grained, full_detail, time_color, title_color))
