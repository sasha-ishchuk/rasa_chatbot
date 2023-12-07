# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions


# This is a simple example for a custom action which utters "Hello World!"

# from typing import Any, Text, Dict, List
#
# from rasa_sdk import Action, Tracker
# from rasa_sdk.executor import CollectingDispatcher
#
#
# class ActionHelloWorld(Action):
#
#     def name(self) -> Text:
#         return "action_hello_world"
#
#     def run(self, dispatcher: CollectingDispatcher,
#             tracker: Tracker,
#             domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:
#
#         dispatcher.utter_message(text="Hello World!")
#
#         return []


import json
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


class ListMenu(Action):
    menu_data = json.loads(Path("data/menu.json").read_text())

    def name(self) -> Text:
        return "action_list_menu"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        menu_items = self.menu_data.get('items')

        if menu_items:
            menu_list = "\nHere is the menu:\n"
            for item in menu_items:
                name = item.get('name')
                price = item.get('price')
                menu_list += f"{name}: ${price}\n"

            dispatcher.utter_message(text=menu_list)
        else:
            dispatcher.utter_message(text="Sorry, the menu is not available at the moment.")

        return []
