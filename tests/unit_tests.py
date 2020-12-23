from PizzaParlour import app
import json
import unittest


class PizzaParlourTest(unittest.TestCase):
    MENU = {
        "menu": {
            "pizza": {
                "size": {
                    "S": 6,
                    "M": 8,
                    "L": 10
                },
                "type": [
                    "Pepperoni",
                    "Margherita",
                    "Vegetarian",
                    "Hawaiian"
                ],
                "toppings": [
                    "Olives",
                    "Basil",
                    "Peppers",
                    "Pineapple",
                    "Ham",
                    "Tomatoes",
                    "Mushrooms",
                    "Jalapenos",
                    "Chicken",
                    "Beef",
                    "Pepperoni"
                ]
            },
            "drinks": {
                "Coke": 2,
                "Diet Coke": 2,
                "Coke Zero": 2,
                "Pepsi": 2,
                "Diet Pepsi": 2,
                "Dr. Pepper": 2,
                "Water": 1,
                "Juice": 3
            }
        }
    }
    ORDER_OBJECT_1 = {"pizza": [{"pizza_size": "M",
                                 "pizza_type": "Margherita",
                                 "toppings": ["Basil", "Chicken"]}],
                      "drink": ["Diet Pepsi"]}
    UPDATED_ORDER_OBJECT_1 = {"pizza": [{"pizza_size": "L",
                                         "pizza_type": "Margherita",
                                         "toppings": ["Basil", "Chicken",
                                                      "Mushrooms"]}],
                              "drink": ["Diet Pepsi", "Coke"]}

    with open("data.json", "r") as file_read:
        ORIGINAL_ORDERS = json.load(file_read)
    file_read.close()

    def _get_data_json(self):
        with open("data.json", "r") as file_read:
            orders = json.load(file_read)
        file_read.close()
        return orders

    def _get_particular_order(self, order_id):
        return app.test_client().get('/orders/{}'.format(order_id))

    def _update_an_order(self, order_id, updated_order):
        return app.test_client().put('/update/{}'.format(order_id),
                                     json=updated_order)

    def _delete_an_order(self, order_id):
        return app.test_client().delete('/delete/{}'.format(order_id))

    def test_1_pizza(self):
        response = app.test_client().get('/pizza')
        assert response.status_code == 200
        assert response.data == b'Welcome to Pizza Planet!'

    def test_2_get_all_orders(self):
        orders = self._get_data_json()
        response = app.test_client().get('/orders/all')
        if len(orders) == 0:
            assert response.status_code == 404
        else:
            assert response.status_code == 200
            data = json.loads(response.get_data(as_text=True))
            return len(data) == len(orders)

    def test_3_create_new_order(self):
        orders = self._get_data_json()
        response = app.test_client().post('/create',
                                          json=PizzaParlourTest.ORDER_OBJECT_1)
        assert response.status_code == 201
        if len(orders) == 0:
            PizzaParlourTest.ORDER_OBJECT_1['id'] = 0
        else:
            PizzaParlourTest.ORDER_OBJECT_1['id'] = orders[-1]['id'] + 1
        data = json.loads(response.get_data(as_text=True))
        assert data == PizzaParlourTest.ORDER_OBJECT_1

    def test_4_get_new_order(self):
        orders = self._get_data_json()
        order_id = orders[-1]['id']
        response = self._get_particular_order(order_id)
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data == PizzaParlourTest.ORDER_OBJECT_1

    def test_5_update_existing_order(self):
        orders = self._get_data_json()
        order_id = orders[-1]['id']
        response = self._update_an_order(order_id,
                                         PizzaParlourTest.
                                         UPDATED_ORDER_OBJECT_1)
        PizzaParlourTest.UPDATED_ORDER_OBJECT_1['id'] = order_id
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data == PizzaParlourTest.UPDATED_ORDER_OBJECT_1

    def test_6_get_new_order_after_update(self):
        orders = self._get_data_json()
        order_id = orders[-1]['id']
        response = self._update_an_order(order_id,
                                         PizzaParlourTest.
                                         UPDATED_ORDER_OBJECT_1)
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data == PizzaParlourTest.UPDATED_ORDER_OBJECT_1

    def test_7_delete_order(self):
        orders = self._get_data_json()
        order_id = orders[-1]['id']
        response = self._delete_an_order(order_id)
        assert response.status_code == 204

    def test_8_get_all_orders_after_delete(self):
        response = app.test_client().get('/orders/all')
        if len(PizzaParlourTest.ORIGINAL_ORDERS) == 0:
            assert response.status_code == 404
        else:
            data = json.loads(response.get_data(as_text=True))
            assert response.status_code == 200
            return data == PizzaParlourTest.ORIGINAL_ORDERS

    def test_9_get_full_menu(self):
        response = app.test_client().get('/menu/full')
        assert response.status_code == 200
        data = json.loads(response.get_data(as_text=True))
        assert data == PizzaParlourTest.MENU

    def test_10_get_menu_pizza_size(self):
        item = {'item': 'S'}
        response = app.test_client().post('/menu/specific', json=item)
        assert response.status_code == 200
        assert response.data == b'Pizzas that are of size S is $6'
        item = {'item': 'M'}
        response = app.test_client().post('/menu/specific', json=item)
        assert response.status_code == 200
        assert response.data == b'Pizzas that are of size M is $8'
        item = {'item': 'L'}
        response = app.test_client().post('/menu/specific', json=item)
        assert response.status_code == 200
        assert response.data == b'Pizzas that are of size L is $10'

    def test_11_get_menu_pizza_toppings(self):
        for topping in PizzaParlourTest.MENU['menu']['pizza']["toppings"]:
            item = {'item': topping}
            response = app.test_client().post('/menu/specific', json=item)
            string_returned = "{} is 2 dollars. So is each other type of" \
                              " additional topping.".format(topping)
            string_returned_bytes = string_returned.encode('UTF-8')
            assert response.status_code == 200
            assert response.data == string_returned_bytes

    def test_12_get_menu_drinks(self):
        for drink in PizzaParlourTest.MENU['menu']['drinks']:
            item = {'item': drink}
            response = app.test_client().post('/menu/specific', json=item)
            string_returned = "{} is ${}".format(
                drink, PizzaParlourTest.MENU['menu']['drinks'][drink])
            string_returned_bytes = string_returned.encode('UTF-8')
            assert response.status_code == 200
            assert response.data == string_returned_bytes
