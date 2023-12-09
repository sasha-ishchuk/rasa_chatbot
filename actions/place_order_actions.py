import json
from pathlib import Path
from typing import Any, Text, Dict, List, Tuple

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


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
