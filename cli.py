import requests
"""
This is the CLI. This class manages users menus, user input, and processing
orders with the API.
"""

# URL for API
PIZZA_PARLOUR_URL = "http://127.0.0.1:5000"

# Opening menu
json_menu = requests.get(PIZZA_PARLOUR_URL + "/menu/full").json()
menu = json_menu['menu']


def cancel_order():
    """
    This function uses stdin to get an order id to delete an order by its
    order id
    """
    delete_id = input("What is the order id of the order "
                      "you would like to delete?\n")

    r = requests.get(PIZZA_PARLOUR_URL + "/orders/all")

    json_orders = []
    if r.status_code == 200:
        json_orders = r.json()

    found = False
    i = 0
    while (not found) and (i < len(json_orders)):
        if delete_id == str(json_orders[i]['id']):
            found = True
            requests.delete(PIZZA_PARLOUR_URL + "/delete/{}".format(
                            delete_id))
            print("Order #" + delete_id + " Successfully cancelled")
        i += 1

    if not found:
        print("Invalid order id")


def get_full_menu():
    """
    Uses the helper functions to the full menu
    """
    pizza = menu['pizza']
    drinks = menu['drinks']
    print(get_menu_sizes(pizza))
    print(get_menu_types(pizza))
    print(get_menu_toppings(pizza))
    print(get_menu_drinks(drinks))


def get_specific_item():
    """
    This function uses stdin to get a item name and calls API to
    get the price of a specific item
    """
    item = input("What item do you want to search?\n")
    out = requests.post(PIZZA_PARLOUR_URL + "/menu/specific",
                        json={"item": item}).text
    print(out)


def get_menu_sizes(pizza) -> str:
    """
    Helper function to print available pizza sizes
    """
    pizza_size = pizza['size']
    ret = ("Here are the sizes for our pizzas. Note that the price of your "
           + "pizza depends on the size and not the type. \n")
    for size in pizza_size:
        ret += ("\t" + size + " is $" + str(pizza_size[size]) + "\n")

    return ret


def get_menu_types(pizza) -> str:
    """
    Helper function to print available pizza types
    """
    pizza_type = pizza['type']
    ret = "The types of pizzas we have are: \n"
    for the_type in pizza_type:
        ret += ("\t" + the_type + "\n")

    return ret


def get_menu_toppings(pizza) -> str:
    """
    Helper function to print available pizza toppings
    """
    pizza_toppings = pizza['toppings']
    ret = "Adding additional toppings are $2 each. Toppings include:\n"
    for topping in pizza_toppings:
        ret += ("\t" + topping + "\n")

    return ret


def get_menu_drinks(drinks) -> str:
    """
    Helper function to print available drinks
    """

    ret = "Here is our drink menu \n"
    for drink in drinks:
        ret += ("\t" + drink + " is $" + str(drinks[drink]) + "\n")

    return ret


def update_order():
    """
    This function takes in stdin to update a corresponding order
    """
    valid_order_num_input = False
    exit_update_order = False
    while not exit_update_order:
        # Get the order number to update
        order_number = input("Enter the id of the order you would you like to "
                             "update\nor \"EXIT\" to exit \n")
        if order_number == "EXIT":
            exit_update_order = True
        elif order_number.isdigit():
            order_with_num_exits = requests.get(PIZZA_PARLOUR_URL + "/orders/"
                                                + order_number.strip())\
                                                .status_code
            if order_with_num_exits == 200:
                valid_order_num_input = True
            else:
                print("Invalid order number. Try again \n")
        else:
            print("Invalid key entered. Try again \n")

        # If we got a valid order number we are going to proceed to ask for
        # user input on what to update
        if valid_order_num_input and (not exit_update_order):
            order = requests.get(PIZZA_PARLOUR_URL + "/orders/"
                                 + order_number).json()
            finished_updating = False
            # Unless the user has specified that they have finished updating
            # the order. This loop with continue
            while not finished_updating:
                # ask about whether the user wants to update the pizza component
                # or drink component
                change_drink_or_pizza = input("What about the order would you "
                                              "like to change? Enter: 1 for "
                                              "pizza, 2 for drink, 0 to exit\n")
                if not change_drink_or_pizza.isdigit():
                    print("Your input is invalid \n")
                elif int(change_drink_or_pizza) == 0:
                    finished_updating = True
                # If the user wants a pizza, we will furthur ask what about the
                # pizza the user wants to update on
                elif int(change_drink_or_pizza) == 1:
                    pizza_index = 0
                    if len(order['pizza']) < 1:
                        print("You don't have a pizza in your order. \n")
                    else:
                        pizza_number_valid = False
                        # Loops until the user specifies which pizza in their
                        # order they want to update
                        while not pizza_number_valid:
                            for i in range(len(order['pizza'])):
                                print(str(i + 1) + ". " + str(order['pizza']
                                                              [i]))
                                print("\n")
                            pizza_to_change = input("Which of the above pizzas "
                                                    "would you like to update? "
                                                    "Please enter the number or"
                                                    " click 0 to exit\n")
                            if not pizza_to_change.isdigit():
                                print("Your input is not valid \n")
                            elif int(pizza_to_change) <= len(order['pizza']):
                                pizza_number_valid = True
                                pizza_index = int(pizza_to_change) - 1
                            else:
                                print("Not a valid number. Please try again\n")
                        finish_pizza_change = False
                        # We loop until the user decides that they have finished
                        # updating the pizza
                        while not finish_pizza_change:
                            pizza_change = input("What would you like to "
                                                 "change about your pizza "
                                                 "order? Enter: 1 for pizza "
                                                 "size, 2 for pizza type, 3 "
                                                 "for pizza toppings, "
                                                 "0 to exit\n")
                            if not pizza_change.isdigit():
                                print(
                                    "Your input is not valid \n"
                                )
                            elif int(pizza_change) == 0:
                                finish_pizza_change = True
                            # Update pizza size
                            elif int(pizza_change) == 1:
                                current_pizza_size = order['pizza'][
                                    pizza_index]["pizza_size"]
                                size = input("Your pizza is of size " +
                                             current_pizza_size +
                                             ". What size would you want to "
                                             "change to change it to? "
                                             "Enter: 1 for S, 2 for M, 3 "
                                             "for L, 0 (or any other key) "
                                             "to exit\n")
                                if not size.isdigit():
                                    pass
                                elif int(size) == 1:
                                    if current_pizza_size == 'S':
                                        print("Your pizza is already "
                                              "a size S. \n")
                                    else:
                                        order['pizza'][
                                            pizza_index]['pizza_size'] = 'S'
                                        print("Order size updated "
                                              "successfully. \n")
                                elif int(size) == 2:
                                    if current_pizza_size == 'M':
                                        print(
                                            "Your pizza is "
                                            "already a size M. \n")
                                    else:
                                        order['pizza'][
                                            pizza_index]['pizza_size'] = 'M'
                                        print("Order size updated "
                                              "successfully. \n")
                                elif int(size) == 3:
                                    if current_pizza_size == 'L':
                                        print(
                                            "Your pizza is "
                                            "already a size L. \n")
                                    else:
                                        order['pizza'][
                                            pizza_index]['pizza_size'] = 'L'
                                        print("Order size updated "
                                              "successfully. \n")
                                else:
                                    pass
                            # Update pizza type
                            elif int(pizza_change) == 2:
                                print("We currently have the"
                                      " following pizzas:\n")
                                pizza_types_in_menu = menu['pizza']['type']
                                for i in range(len(pizza_types_in_menu)):
                                    print(str(i + 1) + ". " +
                                          pizza_types_in_menu[i] +
                                          "\n")
                                print("Your current pizza is a " +
                                      order['pizza'][pizza_index]["pizza_type"]
                                      + " pizza \n")
                                valid_type = False
                                exit_0 = False
                                pizza_type_input = None
                                while (not valid_type) and (not exit_0):
                                    pizza_type_input = input("What would you "
                                                             "like to change "
                                                             "your pizza type "
                                                             "to? Please type "
                                                             "in your choice by"
                                                             " number. Enter 0"
                                                             " to exit\n")
                                    if not pizza_type_input.isdigit():
                                        print("invalid input "
                                              "please try again \n")
                                    elif ((int(pizza_type_input) - 1) in
                                            range(len(pizza_types_in_menu))):
                                        valid_type = True
                                    elif int(pizza_type_input) == 0:
                                        exit_0 = True
                                    else:
                                        print("You did not enter "
                                              "a valid number, please try"
                                              "again.")
                                if valid_type:
                                    if not pizza_type_input.isdigit():
                                        print("Oh no. Something "
                                              "has gone terribly wrong!\n")
                                    else:
                                        new_pizza_type = pizza_types_in_menu[
                                            int(pizza_type_input) - 1]
                                        if new_pizza_type == order['pizza'][
                                                                    pizza_index
                                                                  ][
                                                                  'pizza_type']:
                                            print("Your pizza is already a "
                                                  + new_pizza_type + " "
                                                                     "pizza \n")
                                        else:
                                            print("Your pizza has been updated"
                                                  " successfully \n")
                                            topping_list = order['pizza'][
                                                pizza_index]['toppings']
                                            topping_list.clear()
                                            order['pizza'][pizza_index][
                                                'pizza_type'] = \
                                                new_pizza_type
                                            if new_pizza_type == "Pepperoni":
                                                topping_list.append("Pepperoni")
                                            elif new_pizza_type == "Margherita":
                                                topping_list.append("Basil")
                                            elif new_pizza_type == "Vegetarian":
                                                topping_list.append("Mushrooms")
                                                topping_list.append("Peppers")
                                                topping_list.append("Tomatoes")
                                            elif new_pizza_type == "Hawaiian":
                                                topping_list.append("Pineapple")
                                                topping_list.append("Ham")
                            # Update pizza toppings
                            elif int(pizza_change) == 3:
                                del_or_add_topping = input("What would you like"
                                                           " to do? Enter 1 to "
                                                           "delete a topping 2 "
                                                           "to add a topping, "
                                                           "0 (or any other "
                                                           "key) to exit \n")
                                if not del_or_add_topping.isdigit():
                                    print("invalid input \n")
                                # Delete a topping
                                elif int(del_or_add_topping) == 1:
                                    end_now = False
                                    print("Your current toppings include: ")
                                    for i in range(len(order['pizza'][
                                                           pizza_index]
                                                       ['toppings'])):
                                        print(str(i + 1) + ". ")
                                        print(order['pizza'][pizza_index][
                                                  'toppings'][i] + "\n")
                                    while not end_now:
                                        which_topping = input("Which topping "
                                                              "would you like "
                                                              "to delete? "
                                                              "Please enter "
                                                              "the "
                                                              "corresponding "
                                                              "topping number "
                                                              "or 0 to exit \n")
                                        if not which_topping.isdigit():
                                            print("invalid input \n")
                                        elif int(which_topping) - 1 in \
                                                range(len(order['pizza'][
                                                              pizza_index][
                                                              'toppings'])):
                                            order['pizza'][pizza_index][
                                                'toppings']\
                                                .pop(int(which_topping) - 1)
                                            print("Deleted your topping "
                                                  "successfully! \n")
                                        elif int(which_topping) == 0:
                                            end_now = True
                                        else:
                                            print("Invalid key inputted. "
                                                  "Please try again!")
                                # add a topping
                                elif int(del_or_add_topping) == 2:
                                    index = 1
                                    toppings_in_menu = []
                                    for topping in menu['pizza']['toppings']:
                                        print(str(index) + ". ")
                                        print(topping + "\n")
                                        toppings_in_menu.append(topping)
                                        index += 1
                                    end_now = False
                                    while not end_now:
                                        add_which_topping = input("Please "
                                                                  "indicating "
                                                                  "what topping"
                                                                  " you would "
                                                                  "like to add "
                                                                  "by entering "
                                                                  "the corres"
                                                                  "ponding "
                                                                  "number, "
                                                                  "or 0 to "
                                                                  "exit \n")
                                        if not add_which_topping.isdigit():
                                            print("Invalid key entered"
                                                  ". Please try again \n")
                                        elif int(add_which_topping) - 1 in \
                                                range(
                                                len(toppings_in_menu)):
                                            order['pizza'][pizza_index][
                                                'toppings'].append(
                                                toppings_in_menu[
                                                    int(add_which_topping) - 1])
                                            print("Topping added "
                                                  "successfully \n")
                                            finished_add = input("Would you "
                                                                 "like to "
                                                                 "add another "
                                                                 "topping"
                                                                 "? Please "
                                                                 "enter y for "
                                                                 "yes and any "
                                                                 "other key "
                                                                 " for no.\n")
                                            if finished_add == ("y" or "Y"):
                                                pass
                                            else:
                                                end_now = True
                                        elif int(add_which_topping) == 0:
                                            end_now = True
                                        else:
                                            print("Invalid key inputted. "
                                                  "Please try again!")

                                    else:
                                        pass
                            elif int(pizza_change) == 0:
                                finish_pizza_change = True
                            else:
                                print("Invalid key inputted. Please try again!")
                # modify the drink component of the order
                elif int(change_drink_or_pizza) == 2:
                    drink_change_end = False
                    while not drink_change_end:
                        drink_change = input("Please enter 1 to add a drink, "
                                             "2 to delete a drink"
                                             " and 0 to exit \n")
                        if not drink_change.isdigit():
                            print("Your input is not valid! Try again\n")
                        elif int(drink_change) == 0:
                            drink_change_end = True
                        # add drink(s) to order
                        elif int(drink_change) == 1:
                            drinks_we_have = []
                            drink_index = 1
                            print("We currently have the following drinks: \n")
                            for a_drink in menu['drinks']:
                                drinks_we_have.append(a_drink)
                                print(str(drink_index) + ". " + a_drink + "\n")
                                drink_index += 1
                            finish_adding_drinks = False
                            while not finish_adding_drinks:
                                drink_to_add = input("What drink would you "
                                                     "like to add? Please "
                                                     "enter the corresponding "
                                                     "number or 0 to exit\n")
                                if not drink_to_add.isdigit():
                                    print("Invalid input please try again \n")
                                elif int(drink_to_add) - 1 in range(len(
                                        drinks_we_have)):
                                    order['drink'].append(
                                        drinks_we_have[int(drink_to_add) - 1])
                                    print("Drink added successfully \n")
                                elif int(drink_to_add) == 0:
                                    finish_adding_drinks = True
                                else:
                                    "Invalid input. Please try again \n"
                        # delete drink(s) from order
                        elif int(drink_change) == 2:
                            finished_deleting_drinks = False
                            while not finished_deleting_drinks:
                                print("The drinks you have in your "
                                      "order include: \n")
                                for i in range(len(order['drink'])):
                                    print(str(i + 1) + ". " + order['drink'][
                                        i] + "\n")
                                drink_to_delete = input("Which drink in your "
                                                        "order would you like "
                                                        "to delete? Type in "
                                                        "the corresponding "
                                                        "number or 0 to exit. "
                                                        "If you don't see any "
                                                        "drinks here, your "
                                                        "order does not "
                                                        "currently have drinks "
                                                        "in it. Please "
                                                        "press 0 to exit \n")
                                if not drink_to_delete.isdigit():
                                    print("Invalid input please try again\n")
                                elif int(drink_to_delete) == 0:
                                    finished_deleting_drinks = True
                                elif int(drink_to_delete) - 1 in range(len(
                                        order['drink'])):
                                    order['drink'].pop(int(drink_to_delete) - 1)
                                    print("Drink deleted successfully \n")
                                else:
                                    print("Invalid input. Please try again \n")
                        else:
                            print("invalid input. Please try again \n")

                else:
                    print("Invalid input. Please try again \n")
            # Update the json file
            r = requests.put(PIZZA_PARLOUR_URL + "/update/" + str(order['id']),
                             json=order)
            if r.status_code == 200:
                print("Updated your order successfully \n")
            else:
                print("Cannot update your order \n")


def create_order():
    """
    This function takes required inputs and processes them into an order.
    """
    end = False
    # Empty Order
    new_order = {
        'pizza': [],
        'drink': [],
    }
    # Menu
    while not end:
        x = input("What would you like to add to your order?\n" +
                  "1: Pizza\n" +
                  "2: Drink\n" +
                  "3: View Order\n" +
                  "4: Submit Order\n" +
                  "5: Cancel Order\n")

        # Create Pizza Order
        if x == "1":
            # Pizza size
            new_size = input("Choose a Pizza size\n" +
                             get_menu_sizes(menu['pizza']))
            if new_size in menu['pizza']['size'].keys():
                # Pizza type
                new_pizza_type = input("Choose a Pizza type\n" +
                                       get_menu_types(menu['pizza']))
                if new_pizza_type in menu['pizza']['type']:
                    topping_exit = False
                    topping_list = []
                    # Preparation types, add new preparation style here
                    if new_pizza_type == "Pepperoni":
                        topping_list.append("Pepperoni")
                    elif new_pizza_type == "Margherita":
                        topping_list.append("Basil")
                    elif new_pizza_type == "Vegetarian":
                        topping_list.append("Mushrooms")
                        topping_list.append("Peppers")
                        topping_list.append("Tomatoes")
                    elif new_pizza_type == "Hawaiian":
                        topping_list.append("Pineapple")
                        topping_list.append("Ham")

                    # Additional Toppings
                    while not topping_exit:
                        new_toppings = input("Choose additional toppings, " +
                                             "enter 0 to finish\n" +
                                             get_menu_toppings(menu["pizza"]))
                        if new_toppings == "0":
                            topping_exit = True
                        elif new_toppings in menu['pizza']['toppings']:
                            topping_list.append(new_toppings)
                        else:
                            print("Topping does not exist. Please enter exact "
                                  "name (case sensitive)")

                    # Adding Pizza to new_order
                    new_order['pizza'].append({"pizza_size": new_size,
                                               "pizza_type": new_pizza_type,
                                               "toppings": topping_list})

                    print("Successfully Added")
                else:
                    print("Type does not exist. Please enter exact name "
                          "(case sensitive)")

            else:
                print("Size does not exist. Please enter exact name "
                      "(case sensitive)")

        # Create Drink Order
        elif x == "2":
            new_drink = input("What drink would you like?\n" +
                              get_menu_drinks(menu['drinks']))
            if new_drink in menu['drinks']:
                new_order['drink'].append(new_drink)
                print("Successfully added")
            else:
                print("Drink does not exist. Please enter exact name "
                      "(case sensitive)")

        # Check Current Order
        elif x == "3":
            print(new_order)

        # Submit Order
        elif x == "4":
            # Getting new order id
            new_id = 0
            r = requests.get(PIZZA_PARLOUR_URL + "/orders/all")
            if r.status_code == 200:
                new_id = r.json()[-1]['id'] + 1

            r = requests.post(PIZZA_PARLOUR_URL + "/create", json=new_order)

            if r.status_code == 201:
                # Printing Price and order ID
                print("Success! Your order id is #" + str(
                    new_id) + " totaling $" +
                      str(get_price(new_order)) + "\n")
            else:
                print("Order could not be created\n")

            end = True

        # Cancel Order
        elif x == "5":
            end = True

        # Error Checking
        else:
            print("Invalid input. Try again.")


def view_order():
    """
    This function takes in stdin to print a corresponding order + price
    """
    view_id = input("What is the order id of the order " +
                    "you would like to view?\n")

    r = requests.get(PIZZA_PARLOUR_URL + "/orders/{}".format(view_id))

    if r.status_code == 200:
        order = r.json()
        print(order)
        print("Your order will cost $" + str(get_price(order)))
    else:
        print(r.text)


def get_price(order) -> int:
    """
    This function returns the price of a given order

    :param order: Dictionary:
    :return int:
    """
    price = 0
    # Pizza Pricing
    for pizza in order['pizza']:
        # Size price
        if pizza["pizza_size"] == "S":
            price += 6
        elif pizza["pizza_size"] == "M":
            price += 8
        elif pizza["pizza_size"] == "L":
            price += 10

        # Topping price
        if pizza['pizza_type'] == "Pepperoni":
            price += (len(pizza["toppings"]) - 1) * 2
        elif pizza['pizza_type'] == "Margherita":
            price += (len(pizza["toppings"]) - 1) * 2
        elif pizza['pizza_type'] == "Vegetarian":
            price += (len(pizza["toppings"]) - 3) * 2
        elif pizza['pizza_type'] == "Hawaiian":
            price += (len(pizza["toppings"]) - 2) * 2

    # Drink Pricing
    for drink in order['drink']:
        if drink == "Water":
            price += 1
        elif drink == "Juice":
            price += 3
        else:
            price += 2

    return price


def pickup_or_delivery():
    """
    This function will ask for a specific order number in stdin and what type
    of service option they want. If they choose UberEats or Foodora, it will
    format the data into JSON/CSV respectively and output it to stdout.
    """

    request_id = input("What is the order id of the order you "
                       "would like to request pickup or delivery?\n")

    r = requests.get(PIZZA_PARLOUR_URL + "/orders/{}".format(request_id))

    if r.status_code == 200:
        pd = input("Order Found. Would you like Pickup or Delivery?\n"
                   "1: Pickup\n"
                   "2: Delivery\n")
        if pd == "1":
            print("Thank you. Your order is ready for Pickup\n")
        elif pd == "2":
            address = input("Please enter your Address:\n")
            delivery = input("How would you like for it to be Delivered?\n"
                             "1. UberEats\n"
                             "2. Foodora\n"
                             "ANY. In house delivery\n")

            # Formatting data into json
            delivery_data = {address: {
                "order_details": {"pizza": r.json()['pizza'],
                                  "drink": r.json()["drink"],
                                  "price": get_price(r.json())},
                "order_number": r.json()["id"]}}

            if delivery == "1":
                print("Sending UberEats:\n" + str(delivery_data))
            elif delivery == "2":
                # There is no way I can show all the order details in csv
                # correctly because we can have multiple pizzas and multiple
                # toppings and multiple drinks
                csv_data = "order_details/price,order_number\n" \
                           + str(get_price(r.json())) + "," \
                           + str(r.json()["id"])
                print("Sending Foodora:\n" + str(csv_data))
            else:
                print("Thank you. Delivery on the way to " + address + "\n")

        else:
            print("Invalid input. Try again\n")

    else:
        print(r.text)


def main():
    p = requests.get(PIZZA_PARLOUR_URL + "/pizza").text
    print(p)
    end = False
    while not end:
        number = input("What would you like to like to do today?\n" +
                       "1: Submit an Order\n" +
                       "2: Update an existing order\n" +
                       "3: Cancel order\n" +
                       "4: Request the menu\n" +
                       "5: View an order + Check price\n"
                       "6: Request Pickup or Delivery\n"
                       "9: Exit\n")

        if number == "1":
            create_order()
        elif number == "2":
            update_order()
        elif number == "3":
            cancel_order()
        elif number == "4":
            menu_number = input("1: Full menu\n" +
                                "2: Specific item\n")
            if menu_number == "1":
                get_full_menu()
            elif menu_number == "2":
                get_specific_item()
            else:
                print("Invalid input")
        elif number == "5":
            view_order()
        elif number == "6":
            pickup_or_delivery()
        elif number == "9":
            end = True
        else:
            print("Invalid input. Try again.")


if __name__ == "__main__":
    main()
