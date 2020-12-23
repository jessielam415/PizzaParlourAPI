from flask import Flask, jsonify, request
import json
import string

app = Flask("Assignment 2")


def write_to_json(orders):
    """
    This function writes to our data.json file
    """
    with open('data.json', 'w') as file_out:
        json.dump(orders, file_out)
    file_out.close()


def read_from_json():
    """
    This function reads to our data.json file
    """
    with open("data.json", "r") as file_read:
        orders = json.load(file_read)
    file_read.close()
    return orders


@app.route('/pizza')
def welcome_pizza():
    return 'Welcome to Pizza Planet!'


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_particular_order(order_id):
    """
    Given the order id, the function gets the order from the json
    """
    requested_order = []
    orders = read_from_json()
    for order in orders:
        if order['id'] == order_id:
            requested_order.append(order)
    if len(requested_order) > 0:
        return jsonify(requested_order[0])
    else:
        return "Your order does not exist, please try again", 404


@app.route('/orders/all', methods=['GET'])
def get_all_orders():
    """
    This function gets all the orders in the json file
    """
    orders = read_from_json()
    if len(orders) >= 1:
        return jsonify(orders)
    else:
        return "There are no orders yet", 404


@app.route('/create', methods=['POST'])
def create_new_order():
    """
    This function creates a new order with with the data given
    """
    orders = read_from_json()
    content = request.json
    new_id = 0
    if len(orders) != 0:
        new_id = orders[-1]['id'] + 1
    new_pizza = content['pizza']
    new_drink = content['drink']

    new_order = {
        'id': new_id,
        'pizza':  new_pizza,
        'drink': new_drink
    }
    orders.append(new_order)
    write_to_json(orders)
    return jsonify(new_order), 201


@app.route('/delete/<int:order_id>', methods=['DELETE'])
def delete(order_id):
    """
    Given an order id, this function deletes the corresponding order
    """
    orders = read_from_json()
    order_exists = 0
    i = 0
    for order in orders:
        if order['id'] == order_id:
            order_exists = 1
            break
        i += 1
    if order_exists:
        orders.pop(i)
        write_to_json(orders)
        return "Your order has been deleted", 204
    else:
        return "There was a problem deleting your order", 404


@app.route('/update/<int:order_id>', methods=['PUT'])
def update(order_id):
    """
    Given an order id, This function updates the corresponding orders with
    the given data.
    """
    orders = read_from_json()
    order_exists = 0
    i = 0
    for order in orders:
        if order['id'] == order_id:
            order_exists = 1
            break
        i += 1
    if order_exists:
        content = request.json
        new_pizza = content['pizza']
        new_drink = content['drink']
        orders[i]['pizza'] = new_pizza
        orders[i]['drink'] = new_drink
        write_to_json(orders)
        return jsonify(orders[i])
    else:
        return "There was a problem updating your order", 404


@app.route('/menu/full')
def get_full_menu():
    """
    This function gets the entire menu
    """
    with open(r"menu.json", "r") as file_read:
        menu = json.load(file_read)
    file_read.close()
    print(menu)
    return jsonify(menu)


@app.route('/menu/specific', methods=['POST'])
def get_price_specific():
    """
    This function given an item on the menu will return its price.
    """
    content = request.json
    item = string.capwords(content['item'])
    with open('menu.json', 'r') as json_file:
        json_menu = (json.load(json_file))
    menu = json_menu['menu']
    pizza = menu['pizza']
    pizza_size = pizza['size']
    # pizza_type = pizza['type']
    pizza_toppings = pizza['toppings']
    drinks = menu['drinks']

    if item in pizza_size:
        return "Pizzas that are of size " + item + " is $" \
               + str(pizza_size[item])
    # elif item in pizza_type:
    #     return "All types of pizzas are the same price. " \
    #           "The price depends on the size of the pizza so check for size" \
    #            "instead"
    elif item in pizza_toppings:
        return item + " is 2 dollars. So is each other type of " \
                      "additional topping."
    elif item in drinks:
        return item + " is $" + str(drinks[item])
    else:
        return "You have entered an invalid item. Please try again", 404


if __name__ == "__main__":
    app.run()
