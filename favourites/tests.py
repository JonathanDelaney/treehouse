from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from favourites.models import UsersFavourites
from products.models import Product


class TestFavouritesModels(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword'
        )
        self.product = Product.objects.create(name="test product", price=99.99)
        self.view_favourites = "/favourites/"
        self.add_to_favourites = "/favourites/add/" + str(self.product.id)
        self.remove_from_favourites = "/favourites/remove/" + str(self.product.id)
        self.empty_favourites = "/favourites/"
        self.home = "/home/"
        self.products = "/products/"

    def test_view_favourites_GET(self):
        ''' Test the view favourites view '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.view_favourites)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "favourites/favourites.html")
        self.assertTemplateUsed(response, "base.html")

    def test_add_to_favourites_GET(self):
        ''' Test the add to favourites view GET request '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.add_to_favourites)
        self.assertEqual(response.status_code, 301)

    def test_add_to_favourites_POST(self):
        ''' Test the add to favourites view POST request '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.add_to_favourites)
        favourites = UsersFavourites.objects.get(user=self.user)
        products = favourites.products.all()
        self.assertEqual(response.status_code, 301)

    def test_remove_from_favourites_GET(self):
        ''' Test the remove from favourites view GET request '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.remove_from_favourites)
        self.assertEqual(response.status_code, 301)

    def test_remove_from_favourites_POST(self):
        ''' Test the remove from favourites view POST request '''

        self.client.login(username="testuser", password="testpassword")
        self.client.post(self.add_to_favourites)
        response = self.client.post(self.remove_from_favourites)
        favourites = UsersFavourites.objects.get(user=self.user)
        products = favourites.products.all()
        self.assertFalse(products)

    def test_empty_favourites_GET(self):
        ''' Test the delete favourites view GET request '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.empty_favourites)
        self.assertEqual(response.status_code, 200)

    def test_empty_favourites_POST(self):
        ''' Test the delete favourites view POST request '''

        self.client.login(username="testuser", password="testpassword")
        self.client.post(self.add_to_favourites)
        response = self.client.post(self.empty_favourites)
        favourites = UsersFavourites.objects.get(user=self.user)
        products = favourites.products.all()
        self.assertFalse(products)
