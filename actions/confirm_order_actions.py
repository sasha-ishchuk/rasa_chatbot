# This files contains your custom actions which can be used to run
# custom Python code.
#
# See this guide on how to implement these action:
# https://rasa.com/docs/rasa/custom-actions

import os
import json
from typing import Any, Text, Dict, List
from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ActionOrderConfirmed(Action):
    def name(self) -> Text:
        return "action_order_confirmed"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        file_path = 'data/user_order/user_order.json'

        try:
            with open(file_path, 'r') as file:
                order_data = json.load(file)
                orders = order_data.get("orders", [])

                if orders:
                    for idx, order in enumerate(orders, start=1):
                        dispatcher.utter_message(f"Items: {', '.join(order['items'])}")
                        dispatcher.utter_message(f"Price: {order['price']} USD")
                        dispatcher.utter_message(f"Additional Notes: {', '.join(order['additional_notes'])}\n")
                        dispatcher.utter_message(f"Pick-up your order in {order['time']} hours")
                else:
                    dispatcher.utter_message("No orders found.")

        except FileNotFoundError:
            dispatcher.utter_message(f"File '{file_path}' not found.")
        except json.JSONDecodeError:
            dispatcher.utter_message(f"Error decoding JSON in '{file_path}'.")
        finally:
            file.close()
            os.remove(file_path)

        return []


class ActionDeleteUnconfirmedOrder(Action):
    def name(self) -> Text:
        return "action_delete_unconfirmed_order"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        file_path = 'data/user_order/user_order.json'

        if os.path.exists(file_path):
            os.remove(file_path)

            dispatcher.utter_message("Your order wasn't placed...")

        return []
