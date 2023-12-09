from pathlib import Path
from typing import Any, Text, Dict, List

from rasa_sdk import Action, Tracker
from rasa_sdk.executor import CollectingDispatcher


class ConfirmAdds(Action):
    extra_keywords = Path("data/txt/extra_keywords.txt").read_text().split("\n")
    available_extras = Path("data/txt/available_extras.txt").read_text().split("\n")

    def name(self) -> Text:
        return "action_confirm_adds"

    def run(self, dispatcher: CollectingDispatcher,
            tracker: Tracker,
            domain: Dict[Text, Any]) -> List[Dict[Text, Any]]:

        add_type = tracker.get_slot("type_of_extra_request")
        extra_item = tracker.get_slot("extra_item")

        add = False
        if add_type in self.extra_keywords:
            add = True

        item_present = False
        if extra_item in self.available_extras:
            item_present = True

        if item_present and add:
            dispatcher.utter_message(f"Your order updated. Added note: '{add_type} {extra_item}'.\n")
        elif not item_present:
            dispatcher.utter_message(text="Sorry... We don't have this extra item")
        elif not add and not item_present:
            dispatcher.utter_message(text="Sorry... I don't understood your needs :(")

        return []
