import unittest
import cli

pizza_menu = {
      "size": {
        "L": 10
      },
      "type": [
        "Pepperoni",
      ],
      "toppings": [
        "Beef",
        "Pepperoni"
      ]
    }

drink_menu = {
      "Coke": 2,
      "Diet Coke": 2,
    }


class CLITest(unittest.TestCase):
    def test_get_price(self):
        dict1 = {"id": 0,
                 "pizza": [{"pizza_size": "S",
                            "pizza_type": "Pepperoni",
                            "toppings": ["Pepperoni", "Olives", "Chicken"]}],
                 "drink": ["Coke"]}
        self.assertEqual(cli.get_price(dict1), 12)

    def test_get_menu_sizes(self):
        t = cli.get_menu_sizes(pizza_menu)
        self.assertEqual(t, "Here are the sizes for our pizzas. Note that the"
                            " price of your pizza depends on the size and not "
                            "the type. \n\tL is $10\n")

    def test_get_menu_types(self):
        t = cli.get_menu_types(pizza_menu)
        self.assertEqual(t, "The types of pizzas we have are: \n\tPepperoni\n")

    def test_get_menu_toppings(self):
        t = cli.get_menu_toppings(pizza_menu)
        self.assertEqual(t, "Adding additional toppings are $2 each. Toppings "
                            "include:\n\t" + "Beef\n\t" + "Pepperoni\n")

    def test_get_menu_drinks(self):
        t = cli.get_menu_drinks(drink_menu)
        self.assertEqual(t, "Here is our drink menu \n\tCoke is $2"
                            "\n\tDiet Coke is $2\n")
