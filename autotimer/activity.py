import datetime
import json
from json import JSONDecodeError
from typing import List, Union, Tuple

from dateutil import parser

from settings import ACTIVITIES_JSON_FILE_PATH


class TimeEntry:
    def __init__(self, start_time: datetime.datetime, end_time: datetime.datetime,
                 days: Union[int, None] = None, hours: Union[int, None] = None,
                 minutes: Union[int, None] = None, seconds: Union[int, None] = None):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time

        self.days = self.total_time.days if days is None else days
        self.seconds = self.total_time.seconds if seconds is None else seconds
        self.hours = self.days * 24 + self.seconds // 3600 if hours is None else hours
        self.minutes = (self.seconds % 3600) // 60 if minutes is None else minutes
        self.seconds = self.seconds % 60

    def serialize(self) -> dict:
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }

    @property
    def time_spent(self) -> datetime.timedelta:
        return self.end_time - self.start_time

    def time_spent_in(self,
                      start: datetime.datetime = None,
                      end: datetime.datetime = None) -> datetime.timedelta:
        if start is None:
            start = self.start_time
        if end is None:
            end = self.end_time

        if self.end_time < start or end < self.start_time:
            return datetime.timedelta(0)
        return min(self.end_time, end) - max(self.start_time, start)

    def __str__(self):
        return str(self.time_spent)


class ActivityItem:
    def __init__(self, title: str, time_entries: List[TimeEntry]):
        self.title = title
        self.time_entries = time_entries

    def serialize(self) -> dict:
        return {
            'title': self.title,
            'time_entries': self.make_time_entries_to_json()
        }

    def make_time_entries_to_json(self) -> List[dict]:
        return [time.serialize() for time in self.time_entries]

    @property
    def time_spent(self) -> datetime.timedelta:
        return sum((time_entry.time_spent for time_entry in self.time_entries), datetime.timedelta())

    def time_spent_in(self,
                      start: datetime.datetime = None,
                      end: datetime.datetime = None) -> datetime.timedelta:
        return sum(
            (time_entry.time_spent_in(start, end) for time_entry in self.time_entries),
            datetime.timedelta()
        )

    @property
    def time_interval(self) -> Tuple[datetime.datetime, datetime.datetime]:
        return self.time_entries[0].start_time, self.time_entries[-1].end_time

    @property
    def start_time(self) -> datetime.datetime:
        return self.time_entries[0].start_time

    @property
    def end_time(self) -> datetime.datetime:
        return self.time_entries[-1].end_time

    def __str__(self):
        return '{title}: {time_spent}'.format(title=self.title, time_spent=str(self.time_spent))


class Activity:
    def __init__(self, name: str, items: List[ActivityItem]):
        self.name = name
        self.items = items

    def serialize(self) -> dict:
        return {
            'name': self.name,
            'items': self.make_time_entries_to_json()
        }

    def make_time_entries_to_json(self) -> List[dict]:
        return [item.serialize() for item in self.items]

    @property
    def time_spent(self) -> datetime.timedelta:
        return sum((item.time_spent for item in self.items), datetime.timedelta())

    def time_spent_in(self,
                      start: datetime.datetime = None,
                      end: datetime.datetime = None) -> datetime.timedelta:
        return sum(
            (item.time_spent_in(start, end) for item in self.items
                if ((start is None or start < item.end_time) and
                    (end is None or item.start_time < end))
             ),
            datetime.timedelta()
        )

    @property
    def time_interval(self) -> Tuple[datetime.datetime, datetime.datetime]:
        return self.items[0].start_time, self.items[-1].end_time

    @property
    def start_time(self) -> datetime.datetime:
        return self.items[0].start_time

    @property
    def end_time(self) -> datetime.datetime:
        return self.items[-1].end_time

    def __str__(self):
        return '{name}: {time_spent}'.format(name=self.name, time_spent=str(self.time_spent))


class ActivityList:
    def __init__(self, activity_file: str = ACTIVITIES_JSON_FILE_PATH):
        try:
            with open(activity_file, 'r') as f:
                data = json.load(f)
                self.activities = [
                    Activity(name=activity['name'], items=self.get_activity_items_from_json(activity))
                    for activity in data.get('activities')
                ]
        except FileNotFoundError:
            self.activities = []
        except JSONDecodeError as e:
            print(repr(e))
            print('activities.json is either invalid or empty!')
            self.activities = []

    @staticmethod
    def get_activity_items_from_json(activity_json: dict) -> List[ActivityItem]:
        return [
            ActivityItem(
                title=item['title'],
                time_entries=[
                    TimeEntry(
                        start_time=parser.parse(entry['start_time']),
                        end_time=parser.parse(entry['end_time']),
                        days=entry['days'],
                        hours=entry['hours'],
                        minutes=entry['minutes'],
                        seconds=entry['seconds']
                    ) for entry in item['time_entries']
                ]
            ) for item in activity_json['items']
        ]

    def serialize(self) -> dict:
        return {
            'activities': self.activities_to_json()
        }

    def activities_to_json(self):
        return [activity.serialize() for activity in self.activities]

    @property
    def time_spent(self):
        return sum((activity.time_spent for activity in self.activities), datetime.timedelta())

    def time_spent_in(self,
                      start=None,
                      end=None) -> datetime.timedelta:
        return sum(
            (activity.time_spent_in(start, end) for activity in self.activities
                if ((start is None or start < activity.end_time) and
                    (end is None or activity.start_time < end))
             ),
            datetime.timedelta()
        )

    @property
    def time_interval(self) -> Tuple[datetime.datetime, datetime.datetime]:
        return self.activities[0].start_time, self.activities[-1].end_time

    @property
    def start_time(self) -> datetime.datetime:
        return self.activities[0].start_time

    @property
    def end_time(self) -> datetime.datetime:
        return self.activities[-1].end_time

    def __str__(self):
        return 'Total time: {}'.format(self.time_spent)


def save_activities(activity_list):
    with open(ACTIVITIES_JSON_FILE_PATH, 'w') as json_file:
        json.dump(activity_list.serialize(), json_file,
                  indent=4, sort_keys=False)
