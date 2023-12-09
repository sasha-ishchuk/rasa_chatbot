import json
from datetime import datetime
from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class CheckOpeningHours(Action):
    opening_hours = json.loads(Path("data/opening_hours.json").read_text())

    def name(self) -> Text:
        return "action_check_opening_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get('entities', [])

        for entity in entities:
            if entity['entity'] == 'day_of_week':
                day = entity['value']
                if day in self.opening_hours['items']:
                    dispatcher.utter_message(f"Yes, the restaurant is open on {day}.")
                else:
                    dispatcher.utter_message(f"Sorry, I don't have information about the opening hours for {day}.")

        return []


class CheckOpeningHoursAtTime(Action):
    opening_hours = json.loads(Path("data/opening_hours.json").read_text())

    def name(self) -> Text:
        return "action_check_opening_hours_at_time"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        entities = tracker.latest_message.get('entities', [])

        for entity in entities:
            if entity['entity'] == 'day_of_week':
                day = entity['value']
                if day in self.opening_hours['items']:
                    user_time = int(tracker.get_slot('time'))

                    opening_time = self.opening_hours['items'][day]['open']
                    closing_time = self.opening_hours['items'][day]['close']

                    if opening_time <= user_time <= closing_time:
                        dispatcher.utter_message(f"Yes, the restaurant is open on {day} at {user_time}:00.")
                    else:
                        dispatcher.utter_message(f"Sorry, the restaurant is closed on {day} at {user_time}:00.")
                else:
                    dispatcher.utter_message(f"Sorry, I don't have information about the opening hours for {day}.")

        return []


class CheckOpenNow(Action):
    opening_hours = json.loads(Path("data/opening_hours.json").read_text())

    def name(self) -> Text:
        return "action_check_open_now"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        current_datetime = datetime.now()
        day_of_week = current_datetime.weekday()
        days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']

        day = days_of_week[day_of_week]
        user_time = int(current_datetime.hour)

        if day in self.opening_hours['items']:
            opening_time = self.opening_hours['items'][day]['open']
            closing_time = self.opening_hours['items'][day]['close']

            if opening_time <= user_time <= closing_time:
                dispatcher.utter_message(text="Yes, the restaurant is open now.")
            else:
                dispatcher.utter_message(text="Sorry, the restaurant is closed now.")
        else:
            dispatcher.utter_message(text="Sorry, I don't have information about the opening hours for now.")

        return []
