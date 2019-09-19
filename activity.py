import json
from json import JSONDecodeError

from dateutil import parser

from settings import ACTIVITIES_JSON_FILE_PATH


class ActivityList:
    def __init__(self, activity_file='activities.json'):
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
    def get_activity_items_from_json(activity_json):
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

    def serialize(self):
        return {
            'activities': self.activities_to_json()
        }

    def activities_to_json(self):
        activities_ = []
        for activity in self.activities:
            activities_.append(activity.serialize())

        return activities_


class Activity:
    def __init__(self, name, items):
        self.name = name
        self.items = items

    def serialize(self):
        return {
            'name': self.name,
            'items': self.make_time_entries_to_json()
        }

    def make_time_entries_to_json(self):
        time_list = []
        for time in self.items:
            time_list.append(time.serialize())
        return time_list


class ActivityItem:
    def __init__(self, title,  time_entries):
        self.title = title
        self.time_entries = time_entries

    def serialize(self):
        return {
            'title': self.title,
            'time_entries': self.make_time_entries_to_json()
        }

    def make_time_entries_to_json(self):
        time_list = []
        for time in self.time_entries:
            time_list.append(time.serialize())
        return time_list


class TimeEntry:
    def __init__(self, start_time, end_time, days=None, hours=None, minutes=None, seconds=None):
        self.start_time = start_time
        self.end_time = end_time
        self.total_time = end_time - start_time

        self.days = self.total_time.days if days is None else days
        self.seconds = self.total_time.seconds if seconds is None else seconds
        self.hours = self.days * 24 + self.seconds // 3600 if hours is None else hours
        self.minutes = (self.seconds % 3600) // 60 if minutes is None else minutes
        self.seconds = self.seconds % 60

    def serialize(self):
        return {
            'start_time': self.start_time.strftime("%Y-%m-%d %H:%M:%S"),
            'end_time': self.end_time.strftime("%Y-%m-%d %H:%M:%S"),
            'days': self.days,
            'hours': self.hours,
            'minutes': self.minutes,
            'seconds': self.seconds
        }


def save_activities(activity_list):
    with open(ACTIVITIES_JSON_FILE_PATH, 'w') as json_file:
        json.dump(activity_list.serialize(), json_file,
                  indent=4, sort_keys=False)
