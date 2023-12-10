Rasa based chatbot, which is able to handle customers writing to the restaurant, looking for information and ordering the food. 

### Link to demos: 
* Telegram demo: [telegram demo](https://drive.google.com/file/d/1HEAxxq_zND5yCMtNPghBrS1w0dCq_rXb/view?usp=sharing)
* How typos generator works demo: [typos demo](https://drive.google.com/file/d/1bQD8cO6MLGtEHF5YwrS3QM60OHHulV2f/view?usp=sharing)

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
  - to use the generator you must put the parameters 'file_name' and 'intent_name'
  - script takes all example from the intent and generate 3 variants with mistakes for each example
  - results are printed to stdout, so you can copy/paste it to the intent
* Secondary intents, like greeting or farewell, are handled as well.
* Integrated with Telegram messenger.


### How to run chatbot in terminal
setup/activate environment (if needed):
```
python -m venv ./venv
.\venv\Scripts\activate
```

train chatbot:
```
rasa train
```

run custom actions:
```
rasa run actions
```

run chatbot in terminal (possibly you need to open new terminal window):
```
rasa shell
```

run chatbot with debug option:
```
rasa shell --debug
```


### Integrate with Telegram:

To run chatbot in Telegram follow documentation: [rasa docs](https://rasa.com/docs/rasa/connectors/telegram/)
Here you can find additional explanation: [useful info](https://amilrubasinghe.medium.com/rasa-chatbot-connects-with-your-telegram-account-e2e61f4264d4)

#### Steps:
1. Open Telegram and search BotFather.
2. Start BotFather (/start)
3. Choose option to create new bot (/newbot)
4. Follow BotFather instructions
5. Configure Telegram bot with rasa project 
   - BotFather gives you API credentials and a channel link. 
   - Go to your rasa project and open the ***credentials.yml*** file. 
   - Add a slot for Telegram.
```
telegram:
  access_token: "490161424:AAGlRxinBRtKGb21_rlOEMtDFZMXBl6EC0o"
  verify: "your_bot"
  webhook_url: "https://<your_url.com>/webhooks/telegram/webhook"
```

* **access_token** - BotFather gives you
* **verify** - username you set
* **webhook_url** - replace <your_url.com> with your url

Get your url using ngrok with command: 
```
ngrok http 5005
```

run actions and rasa chatbot (possibly you need to run these commands in 2 terminals):
```
rasa run actions
rasa run
```


### Conversation example:
```
Your input ->  hey

Happy to see you! Welcome to our restaurant :)
What I can do for you?

Your input ->  what you cann?

You can ask me about:
- restaurant opening hours/days of week
- restaurant menu
- placing your order
- add some extras to your food

Your input ->  show menu, pleese

Here is the menu:
Lasagne: $16
Pizza: $12
Hot-dog: $4
Burger: $12.5
Spaghetti Carbonara: $15
Tiramisu: $11

Your input ->  wha the openning houurs?

Mon/Tue/Thu/Fri: 8-20
Wed/Sat: 10-16
Sunday: closed

Your input ->  is rest open now?

Sorry, the restaurant is closed now.
Your input ->  i want order foood
Input your order or choose 'no'.

Your input ->  i need 3 teramisu

The order for 3 Tiramisu(s) is placed. Total price: $33.
Time to prepare: 0.44999999999999996 hour(s).
Something more or any additions?
If no, type 'c' to confirm the order

Your input ->  2 pizza please

The order for 2 Pizza(s) is placed. Total price: $24.
Time to prepare: 1.0 hour(s).
Do you want order something more or maybe you have a special requests?
If no, type 'c' to confirm the order

Your input ->  without garlic

Your order updated. Added note: 'without garlic'.
Something more or any additions?
If no, type 'c' to confirm the order

Your input ->  c

Items: Tiramisu - 3, Pizza - 2
Price: 57.0 USD
Additional Notes: without garlic
---
Pick-up your order in 1.45 hours

Your input ->  thanx

No problem

Your input ->  bey

Ciao
```
