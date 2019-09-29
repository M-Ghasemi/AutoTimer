from activity import ActivityList, Activity, ActivityItem, TimeEntry

spent_time_report = """The time spent on each application and each window."""


def add_to_report(report: str, text: str, indent=""):
    return "{report}\n{indent}{text}".format(indent=indent, report=report, text=text)


def format_hours(name: str, time: str, time_first=True) -> str:
    if time_first:
        return "{}: {}".format(time, name)
    return "{}: {}".format(name, time)


def add_time_entries_to_report(report: str, item: ActivityItem, indent: str):
    for time_entry in item.time_entries:
        report = add_to_report(
            report,
            (time_entry.start_time.strftime("%Y-%m-%d -> from %H:%M:%S ") +
             time_entry.end_time.strftime("to %H:%M:%S")),
            indent)
    return report


def hours_report(activity_list: ActivityList, fine_grained: bool = True, full_detail=False) -> str:
    """If fine_grained is True, the time spent on each window/tab will be included in addition
    to the overall time spent on each application.
    If full_detail is True the exact time spent on each window/tab also will be included."""
    report = spent_time_report
    activity_indent = "\n\r"
    item_indent = "    "

    total_hours = format_hours('Total time spent:', activity_list.time_spent, time_first=False)
    report = add_to_report(report, total_hours, activity_indent)

    for activity in activity_list.activities:
        report = add_to_report(report, activity.name, '\n')
        activity_hours = format_hours('Total time spent', activity.time_spent, time_first=False)
        report = add_to_report(report, activity_hours, item_indent)

        if fine_grained:
            for item in activity.items:
                item_hours = format_hours(item.title, item.time_spent)
                report = add_to_report(report, item_hours, item_indent)
                if full_detail:
                    report = add_time_entries_to_report(report, item, item_indent * 2)

    return report


def print_hours_report(fine_grained: bool = True, full_detail=False):
    print(hours_report(ActivityList(), fine_grained, full_detail))
