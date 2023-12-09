import json
from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


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
