# A2 Pizza Parlour

### Running the Program
Run the main Flask module by running `python3 PizzaParlour.py`

Run the CLI by running `python3 cli.py`

Please run PizzaParlour.py before running cli.py or else it will crash.

#### Installation Guide
##### Virtual Environment
Within project folder 

`python3 -m venv venv`

Activating the environment

`venv/bin/activate`

##### Install Flask

Within the activated environment, use the following command to install Flask:

`pip install Flask`

##### Other installations

We used requests to read from Flask API
`pip install requests`

### Testing the Program
Run unit tests with coverage by running `pytest --cov-report term --cov=. tests/unit_tests.py tests/cli_tests.py`

##### To exclude the venv folder:
Create a .coveragec file containing:
<pre><code>[run]
omit = venv/*</code>></pre>

Then run unit tests with coverage with:

`pytest --cov-config=.coveragec --cov-report term --cov=. tests/unit_tests.py tests/cli_tests.py` 

Note 1: cli_tests.py does not run without PizzaParlour running because cli.py will
crash if PizzaParlour is not running

Note 2: unittests.py are the tests for PizzaParlour.py and cli_tests are for
cli.py. PizzaParlour.py unit test has 94% coverage. However, we could not 
figure out how to use monkeypatch and StringIO to work with cli.py so the 
input/output functions have no unit tests.

### Program Features

Our Pizza Parlour program runs within the command-line interface (CLI) 
implemented with cli.py and interacts with our Flask API for functionality.

#### Main Menu

Upon running cli.py there will be a main menu with 6 options:

1. Submit an Order
2. Update an existing order
3. Cancel order
4. Request the menu
5. View an order + Check price
6. Request Pickup or Delivery

#### Order Submission
This feature asks you what you want in your order. 

**Pizza**

A pizza has 3 predetermined sizes: Small, Medium, Large 
costing $6, $8, $10 respectively. 

Our pizzas have 4 types of preparation (Pepperoni, Margherita, 
Vegetarian, Hawaiian). We decided that each type would have a preset
number of toppings. Pepperoni: Pepperoni; Margherita: Basil;
Vegetarian: Tomatoes, Mushrooms, Peppers; Hawaiian: Pineapple, Ham. To
another pizza type one would need to add an option in this function 
with new preparation.

Upon choose a Pizza type, the user can choose to add additional toppings
to their Pizza, each costing $2 on-top of the Pizza price (Toppings from
Pizza type come free). Adding multiples of the same toppings is allowed
and interpreted as extra toppings.

**Drinks**

We have 8 drinks individually priced (Coke, Coke Zero, Diet Coke, Diet Pepsi,
Dr. Pepper, Juice, Pepsi, Water).

**View Order**

You can view your current order (formatted as a dictionary) and its 
corresponding price.

**Submit Order**

Once you are done with adding Pizza(s) and Drink(s) the Submit Order
feature will submit your order and add it to our order list. This will
also give you your order id and price of order.

#### Updating Order
You can update any component of your order, excluding the delivery and pickup method and details. 
A user is prompted to enter their order id. Then they are asked which component of their order they want to update. They can modify both pizza and drink components. 
If the user decides to modify the pizza component. They are then prompted on what about their pizza they would like to update. They can update the pizza size by changing it to another size. They can update pizza toppings by deleting existing toppings or adding new toppings. The user can also change pizza type. When a user resets pizza type all toppings will be changed to the default toppings of that pizza type. Previously added toppings and toppings that are default in their previous pizza type is removed. 
If a user decides to modify the drink component. They can add new drinks to their order or delete drinks currently in their order.

#### Cancelling Order
This feature will prompt for a valid order id and will promptly delete
that order.

#### Requesting Menu
This feature will have two options:
* Full menu
* Specific item

Full menu will return a formatted full menu

Specific item will prompt for the name of an exact item and return its
corresponding price

#### Viewing Order
This feature will prompt for a valid order id and return a dictionary with
its items and its corresponding price.

#### Requesting Pickup or Delivery
This feature will prompt for a valid order id and ask whether they want
pickup or delivery. If they choose delivery, they will be asked to enter
their address followed by delivery method: UberEats, Foodora, in-house
delivery. If UberEats or Foodora is selected, the program will format
the order into JSON or CSV format respectively and print it to stdout.

### Code Craftsmanship

In order to have good, readable code, we followed many code craftsmanship
guidelines. Each of our functions have a docstring describing the function
and in-line comments to help explain the function's logic.

Our entire code base also follows PEP8 style conventions done through 
Pycharm. Additionally, we used Pylint for linting. 

### Program Design
Our program has a Flask API (PizzaParlour.py) that manages orders and a
command-line interface (cli.py) that uses stdin and stdout to interact
with the Flask API to complete functionality.

In order to format and stylize to our intended level, our CLI has expansive
functions, each of which correspond to a [main menu option](#Main-Menu) to
handle its respective input/output with many helper functions to maintain
single responsibility principle.

Our program was designed to have low coupling and high cohesion with all of
our functions able to run independently, as makes the program more extendable, 
expandable, and testable. 

We wrote functions such as get_price(), get_menu_{}() to complete smaller
tasks to reduce code duplication and maintain single responsibility principle. 

#### Design Patterns
We decided to not use objects to represent pizza and menu in our program because using dictionaries, lists and strings made it very easy for us to send jsonified objects from the the API to the CLI and vice versa. Here is a list of design patterns we made use of in our program: 

Facade:
Our program uses the facade design pattern in our API. The CLI does not need to know the internal workings of the API, it simply makes use of the respective URLs of the API, as well as what to input (in the case of post and put methods) to use all its methods. 

Using the facade design pattern for our API reduces the dependencies our CLI has on our API, creating an organized environment that allows for our API methods to be easily utilized. 

Strategy:
Our program utilizes the strategy pattern in our CLI. Depending on what the user inputs to the CLI, our code executes different algorithms to carry out the respective actions. 
Using the strategy patterns allows for quick selection and execution of the correct code blocks in response to user input. 


### Pair Programming and Reflection

We pair-programmed the get_menu method (later changed to be called get_full_menu) of our original CLI template. We also pair-programmed parts of our API together, including return_full_menu, get_price_specific, the API read and write to JSON file functions. We also pair programmed our menu.json file. 

Here is a breakdown of who the driver and navigator is for the pair-programmed portions:
- Driver: Jessie, Navigator: Frank
  - CLI: get_menu 
  - API: get_price_specific()
  
- Driver: Frank, Navigator: Jessie
  - API: read_from_json(), write_to_json(), return_full_menu()
  - menu.json

Process: 
We started our pair programming first on November 5th, 2020 starting at 3:15 PM. This time was mutually decided upon. Pair programming was done through discord using screen sharing. 
First, Frank was the driver and Jessie was the navigator. Frank started programming the CLI template as we both decided that doing so would give us a good idea of how our API can be developed in a user-friendly manner. Jessie watched Frank program during this period and pointed out some errors in the code that came up while Frank was typing up the code. Then Frank started programming our menu.json file. Jessie provided input on how she thought the menu file should be formatted for easy reference in future use. There was a back and forth conversation between Frank and Jessie on how to structure the menu.json file and eventually the two came to an agreement on how the file should be structuresd. 
Then, we did a switch and Jessie was the driver while Frank was the navigator. Jessie started programming get_menu in the initial CLI template. Frank pointed out a code errors that came up while Jessie was coding. 

On November 6th, we continued our pair programming practice in the evening. Pair programming was also done through discord using screen sharing. Frank and Jessie looked over Jessie's current API code. Frank found and fixed some errors in it. Jessie also found some errors in the current API code and notified Frank to change them. Then, Frank implemented the read_to_json() and write_to_json() functions so that there was data permenance for our orders. Jessie was responsible for looking up how json files are read and written to and instructed Frank on how to write the functions. Afterwards, Frank wrote the return_full_menu function while Jessie made sure there was no errors in the code being written. Then, we did a switch and Jessie began to write the get_price_specific() function. Frank suggested Jessie to not include pizza types in get_price_specific() as all pizza types are the same price based on the size. Jessie then commented out the code. 

Reflection: 
We decided that we enjoyed pair programming as it was reassuring to have another person look over the code as it is being written. We did noticed that we both had errors we did not notice that the other person caught for us. This process resulted in less error in code as it is being written. However, we both also decided that pair programming took up more time than if we were to write the code by ourselves. Another benefit from the pair programming was that we both now have an agreed upon menu.json format that is intuitive to both of us to use in future code, whereas if one person programmed the menu.json on their own, the other person would have to look over it and take additional time in learning how to use it. 
