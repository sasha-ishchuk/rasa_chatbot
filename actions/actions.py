# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import json
from pathlib import Path
from datetime import datetime
from typing import Any, Text, Dict, List, Tuple
from rasa_sdk import Action, Tracker
from rasa_sdk.events import SlotSet
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


class ActionPlaceOrder(Action):
    menu_data = json.loads(Path("data/menu.json").read_text())

    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        quantity = int(tracker.get_slot("quantity"))
        dish_item = tracker.get_slot("dish_item")

        if dish_item:
            total_price, total_time = self.calculate_order(dish_item, quantity)
            dispatcher.utter_message(
                f"The order for {quantity} {dish_item}(s) is placed. Total price: ${total_price}. \n"
                f"Time to prepare: {total_time} hour(s). \n")

        return []

    def calculate_order(self, item: Text, quantity: int) -> Tuple[float, float]:

        total_price = 0
        total_time = 0

        for menu_item in self.menu_data['items']:
            if menu_item['name'].lower() == item.lower():
                item_price = menu_item['price']
                preparation_time = menu_item['preparation_time']
                total_price += item_price * quantity
                total_time += preparation_time * quantity
                break

        return total_price, total_time


class ActionPlaceOrderDefaultOneItem(Action):
    menu_data = json.loads(Path("data/menu.json").read_text())

    def name(self) -> Text:
        return "action_place_order_default_one_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        dish_item = tracker.get_slot("dish_item")
        quantity = 1

        if dish_item:
            total_price, total_time = self.calculate_order(dish_item)
            dispatcher.utter_message(
                f"The order for {quantity} {dish_item}(s) is placed. Total price: ${total_price}. \n"
                f"Time to prepare: {total_time} hour(s). \n")
        return []

    def calculate_order(self, item: Text) -> Tuple[float, float]:
        for menu_item in self.menu_data['items']:
            if menu_item['name'].lower() == item.lower():
                item_price = menu_item['price']
                preparation_time = menu_item['preparation_time']
                return item_price, preparation_time


class ConfirmAdds(Action):
    extra_keywords = Path("data/txt/extra_keywords.txt").read_text().split("\n")
    without_keywords = Path("data/txt/without_keywords.txt").read_text().split("\n")
    available_extras = Path("data/txt/available_extras.txt").read_text().split("\n")

    def name(self) -> Text:
        return "action_confirm_adds"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        add_type = tracker.get_slot("type_of_extra_request")
        extra_item = tracker.get_slot("extra_item")

        add = None
        if add_type in self.extra_keywords:
            add = True
        elif add_type in self.without_keywords:
            add = False

        item_present = False
        if extra_item in self.available_extras:
            item_present = True

        if add is None and not item_present:
            dispatcher.utter_message("Sorry... I don't understood your needs :(")
        elif item_present and add is not None:
            dispatcher.utter_message(f"Your order updated. Added note: '{add_type} {extra_item}'.\n")
        elif not item_present:
            dispatcher.utter_message("Sorry... We don't have this extra item")

        return []

