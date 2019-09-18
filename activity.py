import json
from json import JSONDecodeError

from dateutil import parser


class ActivityList:
    def __init__(self, activity_file='activities.json'):
        try:
            with open(activity_file, 'r') as f:
                data = json.load(f)
                self.activities = [
                    Activity(name=activity['name'], time_entries=self.get_time_entries_from_json(activity))
                    for activity in data.get('activities')
                ]
        except FileNotFoundError:
            self.activities = []
        except JSONDecodeError as e:
            print(repr(e))
            print('activities.json is either invalid or empty!')
            self.activities = []

    @staticmethod
    def get_time_entries_from_json(data):
        return [
            TimeEntry(
                start_time=parser.parse(entry['start_time']),
                end_time=parser.parse(entry['end_time']),
                days=entry['days'],
                hours=entry['hours'],
                minutes=entry['minutes'],
                seconds=entry['seconds']
            ) for entry in data['time_entries']
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
    def __init__(self, name, time_entries):
        self.name = name
        self.time_entries = time_entries

    def serialize(self):
        return {
            'name': self.name,
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
    with open('activities.json', 'w') as json_file:
        json.dump(activity_list.serialize(), json_file,
                  indent=4, sort_keys=True)
