Rasa based chatbot, which is able to handle 
customers writing to the restaurant, looking for information 
and ordering the food. 

### Chatbot is able to handle those interactions:

* Answer the question if the restaurant is open on a given day of week/time.
* List the menu items.
* Place an order - with additional requests (like ‘without garlic’).
* Confirm order.


### Additional features:

* Retrieve information about opening hours and menu from .json files.
* Process the order and confirm purchased meals, as well as additional requests.
  - save order to user_order.json file (temporary file)
  - when user confirm the order temporary file is deleted
* Confirm when the meal will be available as a pick-up in the restaurant. 
* Simple generator, to create the training data with some common typos and language mistakes. 
* Secondary intents, like greeting or farewell, are handled as well.
* Integrated with Telegram messenger.


### Integrate with Telegram: