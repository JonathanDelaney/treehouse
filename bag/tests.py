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
        self.add_to_bag = reverse("add_to_bag", args=[self.product.id])
        self.adjust_bag = reverse("adjust_bag", args=[self.product.id])
        self.remove_from_bag = reverse("remove_from_bag",
                                        args=[self.product.id])

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

    def test_add_to_bag_POST(self):
        ''' test that an product is added to the
         bag and then context is then updated and
         then if the product is added a second time the quantity is updated '''

        response = self.client.post(self.add_to_bag,
                                    data={"quantity": "1",
                                          "redirect_url": "/"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Added test product to your bag")
        response = self.client.post(self.view_bag)
        context = response.context
        self.assertNotEqual(context["bag_items"], [])
        self.assertEqual(context["bag_items"][0]["item_id"],
                         f"{self.product.id}")
        # test that adding the product again updates the quantity
        response = self.client.post(self.add_to_bag,
                                    data={"quantity": 1,
                                          "redirect_url": "/"})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Updated test product's quantity to 2")

    def test_adjust_bag_GET(self):
        ''' test that if the url is typed in
        the user is redirected and an error message is shown '''

        response = self.client.get(self.adjust_bag)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Error, you do not have permission to do this.")

    def test_adjust_bag_POST(self):
        ''' test the bag is updated upon posting a new quantity
        and if the quantity is set to 0 the item is removed '''

        response = self.client.post(self.adjust_bag,
                                    data={"quantity": 2})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Updated test product quantity to 2")
        response = self.client.post(self.view_bag)
        context = response.context
        self.assertNotEqual(context["bag_items"], [])
        self.assertEqual(context["bag_items"][0]["quantity"], 2)

        # test bag empties when quantity set to 0
        response = self.client.post(self.adjust_bag,
                                    data={"quantity": 0})
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Removed test product from your bag")
        response = self.client.post(self.view_bag)
        context = response.context
        self.assertEqual(context["bag_items"], [])

    def test_remove_from_bag_GET(self):
        ''' test that when the url is typed into the browser
        the user is redirected and an error message is shown '''

        response = self.client.get(self.remove_from_bag)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Error, you do not have permission to do this.")

    def test_remove_from_bag_POST(self):
        ''' test that the itemms are removed from the bag '''

        # adding items to bag first
        self.client.post(self.adjust_bag,
                         data={"quantity": 1})
        response = self.client.post(self.remove_from_bag)
        messages = list(get_messages(response.wsgi_request))

        # second message as adding to the bag also adds a message
        self.assertEqual(len(messages), 2)
        self.assertEqual(str(messages[1]),
                         "Removed test product from your bag")
        response = self.client.post(self.view_bag)
        context = response.context
        self.assertEqual(context["bag_items"], [])

    def test_remove_from_bag_POST_exception(self):
        ''' test the exception by trying to remove
        from an empty bag '''

        response = self.client.post(self.remove_from_bag)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Error removing item: '1'")
        response = self.client.post(self.view_bag)
        context = response.context
        self.assertEqual(context["bag_items"], [])
