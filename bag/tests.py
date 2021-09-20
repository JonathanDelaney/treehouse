from django.test import TestCase, Client
from django.urls import reverse
from products.models import Product
from django.contrib.messages import get_messages


class TestBagViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.home = reverse("home")
        self.view_bag = reverse("view_bag")
        self.product = Product.objects.create(name="test product", price="1")
        self.add_to_bag = reverse("add_to_bag", kwargs={"product_id": self.product.id})
        self.update_bag = reverse("adjust_bag",
                                   kwargs={"product_id": self.product.id})
        self.remove_from_bag = reverse("remove_from_bag",
                                        kwargs={"product_id": self.product.id})

    def test_view_bag_view_GET(self):
        ''' test the view bag page  '''

        response = self.client.get(self.view_bag)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "bag/bag.html")
        self.assertTemplateUsed(response, "base.html")

    def test_add_to_bag_GET(self):
        ''' test that if the url is typed
        into the browser the user is redirected
        and an error message is shown  '''

        response = self.client.get(self.add_to_bag)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Error you do not have permission to do this.")
