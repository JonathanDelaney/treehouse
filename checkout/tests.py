from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product
from django.contrib.auth.models import User
from django.contrib.messages import get_messages


class TestCheckoutViews(TestCase):

    def setUp(self):

        self.client = Client()
        self.checkout = reverse("checkout")
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testPassword'
        )
        self.product = Product.objects.create(name="test product", price="1")
        self.add_to_bag = reverse("add_to_bag", args=[self.product.id])

    def test_checkout_view_with_empty_cart(self):
        ''' Test the checkout view with an empty cart. '''

        response = self.client.get(self.checkout)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "There's nothing in your bag at the moment")

    def test_checkout_view_with_cart(self):
        ''' Test the checkout view with a =n product in the cart '''

        self.client.post(self.add_to_bag,
                         data={"quantity": "1",
                               "redirect_url": "/"})
        response = self.client.get(self.checkout)
        self.assertEqual(response.status_code, 200)

    def test_checkout_success(self):
        ''' Test the checkout success view. '''

        self.client.post(self.add_to_bag,
                         data={"quantity": "1",
                               "redirect_url": "/"})
        response = self.client.post(self.checkout,
                                    data={
                                        'full_name': 'testuser',
                                        'email': 'test@email.com',
                                        'phone_number': '0873534365',
                                        'street_address1': 'main st',
                                        'street_address2': '',
                                        'town_or_city': 'dublin',
                                        'county': 'dublin',
                                        'postcode': '',
                                        'country': 'IE',
                                        'client_secret': 'client',
                                    }, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'checkout/checkout_success.html')

    def test_checkout_view_with_form_prefilled(self):
        ''' Test the checkout view form is prefilled
            With the user data'''

        self.client.post(self.add_to_bag,
                         data={"quantity": "1",
                               "redirect_url": "/"})
        self.client.login(username="testuser", password="testPassword")
        response = self.client.get(self.checkout)
        self.assertEqual(response.status_code, 200)
