import json
import os


def overwrite_orders_with_new_order():
    file_path = 'data/user_order/user_order.json'

    new_order = {
        "items": [],
        "price": 0.0,
        "time": 0.0,
        "additional_notes": []
    }

    updated_data = {
        "orders": [new_order]
    }

    with open(file_path, 'w') as file:
        json.dump(updated_data, file, indent=4)


def append_to_last_order_items(item, price, time):
    file_path = 'data/user_order/user_order.json'

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
            orders = existing_data.get("orders", [])

            if orders:
                last_order = orders[-1]  # Retrieve the last order from the array
                last_order_items = last_order.get("items", [])
                last_order_items.append(item)
                last_order["items"] = last_order_items

                last_order["price"] += price
                last_order["time"] += time

                with open(file_path, 'w') as file1:
                    json.dump(existing_data, file1, indent=4)
            else:
                print("No orders found in the file.")
    else:
        print("The file does not exist or is empty.")


def append_to_last_order_note(note):
    file_path = 'data/user_order/user_order.json'

    if os.path.exists(file_path) and os.path.getsize(file_path) > 0:
        with open(file_path, 'r') as file:
            existing_data = json.load(file)
            orders = existing_data.get("orders", [])

            if orders:
                last_order = orders[-1]  # Retrieve the last order from the array
                last_order_notes = last_order.get("additional_notes", [])
                last_order_notes.append(note)
                last_order["additional_notes"] = last_order_notes

                with open(file_path, 'w') as file1:
                    json.dump(existing_data, file1, indent=4)
            else:
                print("No orders found in the file.")
    else:
        print("The file does not exist or is empty.")


