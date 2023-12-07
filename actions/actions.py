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
from typing import Any, Text, Dict, List, Tuple
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher
import logging

# Create a logger
logger = logging.getLogger(__name__)


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


class ActionPlaceOrder(Action):

    menu_data = json.loads(Path("data/menu.json").read_text())

    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract entities from user input
        quantity = int(tracker.get_slot("quantity"))
        dish_item = tracker.get_slot("dish_item")

        # Your logic for processing the order
        if dish_item:
            total_price, total_time = self.calculate_order(dish_item, quantity)
            dispatcher.utter_message(f"The order for {quantity} {dish_item}(s) is placed. Total price: ${total_price}. \n"
                                     f"Time to prepare: {total_time} hour(s). We'll be waiting you pick-up your order!")

        return []

    def calculate_order(self, item: Text, quantity: int) -> Tuple[float, float]:
        # Load menu data from menu.json file
        # with open('menu.json', 'r') as file:
        #     menu_data = json.load(file)

        # Initialize variables for total price and total time
        total_price = 0
        total_time = 0

        # Search for the selected item in the menu and calculate total price and time
        for menu_item in self.menu_data['items']:
            if menu_item['name'].lower() == item.lower():
                item_price = menu_item['price']
                preparation_time = menu_item['preparation_time']

                # Calculate total price and total time based on quantity
                total_price += item_price * quantity
                total_time += preparation_time * quantity

                break  # Stop loop once the item is found

        return total_price, total_time


class ActionPlaceOrderDefaultOneItem(Action):

    menu_data = json.loads(Path("data/menu.json").read_text())

    def name(self) -> Text:
        return "action_place_order_default_one_item"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        # Extract entities from user input
        dish_item = tracker.get_slot("dish_item")

        quantity = 1

        if dish_item:
            total_price, total_time = self.calculate_order(dish_item)
            dispatcher.utter_message(f"The order for {quantity} {dish_item}(s) is placed. Total price: ${total_price}. \n"
                                     f"Time to prepare: {total_time} hour(s). We'll be waiting you pick-up your order!")
        return []

    def calculate_order(self, item: Text) -> Tuple[float, float]:
        for menu_item in self.menu_data['items']:
            if menu_item['name'].lower() == item.lower():
                item_price = menu_item['price']
                preparation_time = menu_item['preparation_time']
                return item_price, preparation_time
