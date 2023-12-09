Rasa based chatbot, which is able to handle 
customers writing to the restaurant, looking for information 
and ordering the food. 

### Chatbot is able to handle those interactions:

* Answer the question if the restaurant is open on a given day of week/time.
* List the menu items.
* Place an order - with possibility that the order will contain items not listed on the menu, or additional requests (like ‘without the tomatoes’).


___
* For each of our main intents (mentioned above), it is required to write a simple generator, to create the training dataset with some common typos and language mistakes. Please feel free to choose the cases you want to handle. Apart from those, we should include the secondary intents, like greeting or farewell, to be handled as well.
* During the exercise you may find the following Rasa functionalities useful:

