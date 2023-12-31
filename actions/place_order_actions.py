import json
from pathlib import Path
from typing import Any, Text, Dict, List, Tuple

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher

import os

from save_order import overwrite_orders_with_new_order, append_to_last_order_items

file_path = 'data/user_order/user_order.json'


class ActionPlaceOrder(Action):
    menu_data = json.loads(Path("data/menu.json").read_text())

    def name(self) -> Text:
        return "action_place_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        q = tracker.get_slot("quantity")
        quantity = 1
        if q is not None:
            quantity = int(q)
        dish_item = tracker.get_slot("dish_item")

        if dish_item:
            total_price, total_time = self.calculate_order(dish_item, quantity)
            if not os.path.exists(file_path):
                overwrite_orders_with_new_order()

            if total_time == 0 and total_price == 0:
                dispatcher.utter_message(f"Sorry, we don't have {dish_item} in our menu. \n")
            else:
                item = dish_item + " - " + str(quantity)
                append_to_last_order_items(item, total_price, total_time)

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

            if not os.path.exists(file_path):
                overwrite_orders_with_new_order()

            if total_time == 0 and total_price == 0:
                dispatcher.utter_message(f"Sorry, we don't have {dish_item} in our menu. \n")
            else:
                item = dish_item + " - " + str(quantity)
                append_to_last_order_items(item, total_price, total_time)

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
