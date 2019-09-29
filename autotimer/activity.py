import json
import datetime

from json import JSONDecodeError
from dateutil import parser
from typing import List, Union
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

    def __str__(self):
        return str(self.time_spent)


class ActivityItem:
    def __init__(self, title: str,  time_entries: List[TimeEntry]):
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

    def __str__(self):
        return 'Total time: {}'.format(self.time_spent)


def save_activities(activity_list):
    with open(ACTIVITIES_JSON_FILE_PATH, 'w') as json_file:
        json.dump(activity_list.serialize(), json_file,
                  indent=4, sort_keys=False)
