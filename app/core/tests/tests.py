import json
from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User, Group

from ..models import AvailableToppings, PizzaMasterPieces


class PizzaAppTests(TestCase):
    def setUp(self):
        self.client = Client()

        # Create groups for testing
        self.group_owner = Group.objects.create(name='Pizza Store Owner')
        self.group_chef = Group.objects.create(name='Pizza Chef')

        # Create users
        self.user_owner = User.objects.create_user(username='owner', password='password')
        self.user_owner.groups.add(self.group_owner)

        self.user_chef = User.objects.create_user(username='chef', password='password')
        self.user_chef.groups.add(self.group_chef)

        self.user_normal = User.objects.create_user(username='normal', password='password')

    # --------------------
    # HomePageView tests
    # --------------------
    def test_home_page_view_authenticated(self):
        """Ensure logged-in users can access home and the context contains pizza_list."""
        self.client.force_login(self.user_normal)
        # Create a sample pizza
        PizzaMasterPieces.objects.create(pizza_name="Test Pizza")
        response = self.client.get(reverse('home'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('pizza_list', response.context)

    # --------------------
    # ToppingsPageView tests
    # --------------------
    def test_toppings_page_view_owner(self):
        """Owner should be able to view toppings page and see available toppings in context."""
        self.client.force_login(self.user_owner)
        # Create a sample topping
        AvailableToppings.objects.create(topping_name="Pepperoni", available=True)
        response = self.client.get(reverse('available_toppings'))
        self.assertEqual(response.status_code, 200)
        self.assertIn('available_toppings', response.context)

    def test_toppings_page_view_non_owner(self):
        """Non-owner user should not be allowed to view the toppings page."""
        self.client.force_login(self.user_normal)
        response = self.client.get(reverse('available_toppings'))
        # Depending on your group_required decorator, you might get a redirect or 403.
        self.assertNotEqual(response.status_code, 200)

    # --------------------
    # Topping management view tests
    # --------------------
    def test_add_new_topping(self):
        """Test adding a new topping via POST."""
        self.client.force_login(self.user_owner)
        data = {
            'topping_name': 'Mushrooms',
            'available': 'True'
        }
        response = self.client.post(reverse('add_new_topping'), data)
        self.assertEqual(response.status_code, 200)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        self.assertEqual(json_response.get('toppingName'), 'Mushrooms'.title())

    def test_add_new_topping_invalid_method(self):
        """GET request should return error for add_new_topping view."""
        self.client.force_login(self.user_owner)
        response = self.client.get(reverse('add_new_topping'))
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    def test_update_topping_status(self):
        """Test updating topping availability."""
        self.client.force_login(self.user_owner)
        topping = AvailableToppings.objects.create(topping_name='Onions', available=True)
        data = {
            'topping_name': 'Onions',
            'available': 'false'
        }
        response = self.client.post(reverse('update_topping_status'), data)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        topping.refresh_from_db()
        self.assertFalse(topping.available)

    def test_update_topping_status_not_found(self):
        """Test update when the topping does not exist."""
        self.client.force_login(self.user_owner)
        data = {
            'topping_name': 'NonExistent',
            'available': 'true'
        }
        response = self.client.post(reverse('update_topping_status'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    def test_delete_existing_topping(self):
        """Test deleting an existing topping."""
        self.client.force_login(self.user_owner)
        topping = AvailableToppings.objects.create(topping_name='Olives', available=True)
        data = {'topping_name': 'Olives'}
        response = self.client.post(reverse('delete_existing_topping'), data)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        self.assertFalse(AvailableToppings.objects.filter(topping_name='Olives').exists())

    def test_delete_existing_topping_not_found(self):
        """Test deleting a topping that does not exist."""
        self.client.force_login(self.user_owner)
        data = {'topping_name': 'NonExistent'}
        response = self.client.post(reverse('delete_existing_topping'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    def test_update_existing_topping(self):
        """Test updating an existing topping's details."""
        self.client.force_login(self.user_owner)
        AvailableToppings.objects.create(topping_name='Bacon', available=True)
        data = {
            'original_topping_name': 'Bacon',
            'new_topping_name': 'Turkey',
            'new_availability': 'False'
        }
        response = self.client.post(reverse('update_existing_topping'), data)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        topping = AvailableToppings.objects.get(topping_name='Turkey')
        self.assertEqual(topping.topping_name, 'Turkey')

    def test_update_existing_topping_not_found(self):
        """Test updating a topping that does not exist."""
        self.client.force_login(self.user_owner)
        data = {
            'original_topping_name': 'NonExistent',
            'new_topping_name': 'NewName',
            'new_availability': 'True'
        }
        response = self.client.post(reverse('update_existing_topping'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    # --------------------
    # Toppings retrieval tests
    # --------------------
    def test_get_available_toppings(self):
        """Test that only toppings with available=True are returned."""
        self.client.force_login(self.user_owner)
        AvailableToppings.objects.create(topping_name='Cheese', available=True)
        AvailableToppings.objects.create(topping_name='Tomato', available=False)
        response = self.client.get(reverse('get_available_toppings'))
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        self.assertEqual(len(json_response.get('toppings')), 1)

    def test_get_unavailable_toppings(self):
        """Test that only toppings with available=False are returned."""
        self.client.force_login(self.user_chef)
        AvailableToppings.objects.create(topping_name='Pepper', available=False)
        AvailableToppings.objects.create(topping_name='Olive', available=True)
        response = self.client.get(reverse('get_unavailable_toppings'))
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        self.assertEqual(len(json_response.get('toppings')), 1)

    # --------------------
    # Pizza retrieval and management tests
    # --------------------
    def test_get_all_pizzas(self):
        """Test retrieval of all pizzas with their toppings."""
        self.client.force_login(self.user_chef)
        topping1 = AvailableToppings.objects.create(topping_name='Spinach', available=True)
        topping2 = AvailableToppings.objects.create(topping_name='Mushrooms', available=True)
        pizza = PizzaMasterPieces.objects.create(pizza_name='Veggie Pizza')
        pizza.toppings.add(topping1, topping2)
        response = self.client.get(reverse('get_all_pizzas'))
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        self.assertEqual(len(json_response.get('pizzas')), 1)
        self.assertEqual(json_response.get('pizzas')[0]['pizzaName'], 'Veggie Pizza')

    def test_create_new_pizza(self):
        """Test creating a new pizza with valid data."""
        self.client.force_login(self.user_chef)
        topping1 = AvailableToppings.objects.create(topping_name='Mushrooms', available=True)
        topping2 = AvailableToppings.objects.create(topping_name='Olives', available=True)
        data = {
            'pizza-name': 'New Pizza',
            'topping-list': [topping1.topping_name, topping2.topping_name]
        }
        response = self.client.post(reverse('create_new_pizza'), data)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        self.assertEqual(json_response.get('pizza_name'), 'New Pizza'.title())

    def test_create_duplicate_pizza(self):
        """Test that a duplicate pizza (by toppings) is not created."""
        self.client.force_login(self.user_chef)
        topping1 = AvailableToppings.objects.create(topping_name='Mushrooms', available=True)
        data = {
            'pizza-name': 'Duplicate Pizza',
            'topping-list': [topping1.topping_name]
        }
        # Create an initial pizza with the same topping
        pizza = PizzaMasterPieces.objects.create(pizza_name='Duplicate Pizza')
        pizza.toppings.add(topping1)
        response = self.client.post(reverse('create_new_pizza'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    def test_create_new_pizza_missing_data(self):
        """Test that missing pizza name or toppings returns an error."""
        self.client.force_login(self.user_chef)
        data = {
            'pizza-name': '',
            'topping-list': []
        }
        response = self.client.post(reverse('create_new_pizza'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    def test_delete_existing_pizza(self):
        """Test deleting an existing pizza."""
        self.client.force_login(self.user_chef)
        pizza = PizzaMasterPieces.objects.create(pizza_name='Pizza To Delete')
        data = {'pizza_name': 'Pizza To Delete'}
        response = self.client.post(reverse('delete_existing_pizza'), data)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        self.assertFalse(PizzaMasterPieces.objects.filter(pizza_name='Pizza To Delete').exists())

    def test_delete_existing_pizza_not_found(self):
        """Test deleting a pizza that does not exist."""
        self.client.force_login(self.user_chef)
        data = {'pizza_name': 'NonExistent Pizza'}
        response = self.client.post(reverse('delete_existing_pizza'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    def test_update_pizza_details(self):
        """Test updating a pizza's name."""
        self.client.force_login(self.user_chef)
        pizza = PizzaMasterPieces.objects.create(pizza_name='Old Pizza')
        data = {
            'original_pizza_name': 'Old Pizza',
            'new_pizza_name': 'Updated Pizza'
        }
        response = self.client.post(reverse('update_pizza_details'), data)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        pizza.refresh_from_db()
        self.assertEqual(pizza.pizza_name, 'Updated Pizza'.title())

    def test_update_pizza_details_not_found(self):
        """Test updating details for a non-existent pizza."""
        self.client.force_login(self.user_chef)
        data = {
            'original_pizza_name': 'NonExistent',
            'new_pizza_name': 'New Name'
        }
        response = self.client.post(reverse('update_pizza_details'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))

    def test_update_pizza_toppings(self):
        """Test updating a pizza’s toppings."""
        self.client.force_login(self.user_chef)
        topping1 = AvailableToppings.objects.create(topping_name='Mushrooms', available=True)
        topping2 = AvailableToppings.objects.create(topping_name='Olives', available=True)
        pizza = PizzaMasterPieces.objects.create(pizza_name='Test Pizza')
        pizza.toppings.add(topping1)
        data = {
            'pizza_name': 'Test Pizza',
            'topping_list': json.dumps([topping2.topping_name])
        }
        response = self.client.post(reverse('update_pizza_toppings'), data)
        json_response = response.json()
        self.assertTrue(json_response.get('success'))
        pizza.refresh_from_db()
        toppings = list(pizza.toppings.all())
        self.assertEqual(len(toppings), 1)
        self.assertEqual(toppings[0].topping_name, topping2.topping_name)

    def test_update_pizza_toppings_duplicate(self):
        """Test that updating a pizza’s toppings to a combination that already exists returns an error."""
        self.client.force_login(self.user_chef)
        topping = AvailableToppings.objects.create(topping_name='Mushrooms', available=True)
        # Create a pizza with this topping combination
        pizza1 = PizzaMasterPieces.objects.create(pizza_name='Existing Pizza')
        pizza1.toppings.add(topping)
        # Create another pizza to update
        pizza2 = PizzaMasterPieces.objects.create(pizza_name='Update Pizza')
        pizza2.toppings.clear()
        data = {
            'pizza_name': 'Update Pizza',
            'topping_list': json.dumps([topping.topping_name])
        }
        response = self.client.post(reverse('update_pizza_toppings'), data)
        json_response = response.json()
        self.assertFalse(json_response.get('success'))
