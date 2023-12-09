import json
from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ListMenu(Action):
    open_hours_data = json.loads(Path("data/opening_hours.json").read_text())

    def name(self) -> Text:
        return "action_list_opening_hours"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        open_list = "\nOur opening hours:\n"

        for day, hours in self.open_hours_data['items'].items():
            open_list += f"{day}: {hours['open']} - {hours['close']}\n"

        dispatcher.utter_message(text=open_list)

        return []
