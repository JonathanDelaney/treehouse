from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from .models import Product, Category

# Create your tests here.


class TestProductsViews(TestCase):
    "test the stock views for all users"

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword'
        )
        self.category = Category.objects.create(
            name="test_categories",
            friendly_name="Test Categories"
        )
        self.product = Product.objects.create(
            sku="1",
            name="test product",
            description="test description",
            price=2.99,
            category=self.category,
            rating=4.6,
            image_url="http://test.com/image/.jpg",
            image="testimage.jpg",
        )
        self.products = reverse("products")
        self.product_detail = reverse("product_detail",
                                   args=[self.product.id])

    def test_all_products_view(self):
        ''' Test the all products view '''

        response = self.client.get(self.products)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/products.html")
        self.assertTemplateUsed(response, "base.html")

    def test_all_products_views_with_query(self):
        ''' Test the all products view with a query parameter '''

        response = self.client.get(self.products,
                                   {"query": "test"})
        context = response.context
        self.assertTrue('query')

    def test_all_products_views_with_categories(self):
        ''' Test the all products view with a category parameter '''

        response = self.client.get(self.products,
                                   {"category": "test_categories"})
        category = Category.objects.get(name="test_categories")
        context = response.context
        self.assertTrue(context['current_categories'])

    def test_all_products_views_with_sort(self):
        '''  Test the all products view with a sort paramater '''

        response = self.client.get(self.products,
                                   {"sort": "name"})
        context = response.context
        self.assertTrue(context['sort'])
        self.assertEqual(context['sort'], "name")

    def test_all_products_views_with_direction(self):
        ''' Test the all products view with a direction parameter '''

        response = self.client.get(self.products,
                                   {"sort": "name",
                                    "direction": "desc"})
        context = response.context
        self.assertTrue(context['direction'])
        self.assertEqual(context['direction'], "desc")

    def test_view_product_detail_view(self):
        ''' Test the single product view '''
        response = self.client.get(self.product_detail)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/product_detail.html")
        self.assertTemplateUsed(response, "base.html")


class TestStockControl(TestCase):

    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword'
        )
        self.super_user = User.objects.create_superuser(
            username='testadmin',
            email='testadmin@email.com',
            password='testadminpassword'
        )
        self.category = Category.objects.create(
            name="test_categories",
            friendly_name="Test Categories"
        )
        self.product = Product.objects.create(
            sku="1",
            name="test product",
            description="test description",
            price=2.99,
            category=self.category,
            rating=4.6,
            image_url="http://test.com/image/.jpg",
            image="testimage.jpg",
        )
        self.products = reverse("products")
        self.product_detail = reverse("product_detail",
                                   kwargs={"product_id": self.product.id})
        self.add_product = reverse("add_product")
        self.home = reverse("home")
        self.edit_product = reverse("edit_product", kwargs={"product_id": self.product.id})
        self.delete_product = reverse("delete_product",
                                   kwargs={"product_id": self.product.id})

    def test_add_product_not_supperuser(self):
        ''' Test the add product view if the user is not a superuser '''

        self.client.login(
            username="testuser", password="testpassword")
        response = self.client.get(self.add_product)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Sorry, only store owners can do that.")

    def test_add_product_GET_supperuser(self):
        ''' Test the add product get if not a superuser '''

        self.client.login(
            username="testadmin", password="testadminpassword")
        response = self.client.get(self.add_product)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/add_product.html")
        self.assertTemplateUsed(response, "base.html")

    def test_add_product_POST_invalidform(self):
        ''' Test the add product with an invalid form '''

        self.client.login(
            username="testadmin", password="testadminpassword")
        response = self.client.post(self.add_product, {
            "code": "",
            "name": "",
            "description": "",
            "price": "",
            "category": self.category,
        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Failed to add product. \
                Please ensure the form is valid.")

    def test_add_product_POST_validform(self):
        ''' test the add product with a valid form '''

        self.client.login(
            username="testadmin", password="testadminpassword")
        response = self.client.post(self.add_product, {
            "name": "Test",
            "description": "test description",
            "price": 2.99,
         })
        product = Product.objects.get(name="Test")
        self.assertTrue(product)
        self.assertEqual(product.description, 'test description')
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Successfully added product!")

    def test_edit_post_if_not_superuser(self):
        ''' Test the edit post view if not a superuser '''

        self.client.login(
            username="testuser", password="testpassword")
        response = self.client.get(self.edit_product)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Sorry, only store owners can do that.")

    def test_edit_product_GET_if_superuser(self):
        ''' Test the edit product get if superuser '''

        self.client.login(
            username="testadmin", password="testadminpassword")
        response = self.client.get(self.edit_product)
        self.assertEqual(response.context['form'].initial['name'],
                         self.product.name)
        self.assertEqual(response.context['form'].initial['description'],
                         self.product.description)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "products/edit_product.html")
        self.assertTemplateUsed(response, "base.html")

    def test_edit_product_POST_invalidform(self):
        ''' test the edit product view post with invalid form'''

        self.client.login(
            username="testadmin", password="testadminpassword")

        response = self.client.post(self.edit_product, {

        })
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Failed to update product. \
Please ensure the form is valid.")

    def test_edit_product_POST_validform(self):
        ''' Test edit product view with a valid form '''

        self.client.login(
            username="testadmin", password="testadminpassword")
        response = self.client.post(self.edit_product, {
            "name": "Test editing",
            "description": "test description edited",
            "price": 100.00,
            }
        )
        product = Product.objects.get(id=self.product.id)
        self.assertEqual(product.description, 'test description edited')
        self.assertEqual(product.price, 100.00)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Successfully updated product!")

    def test_delete_product_if_not_superuser(self):
        ''' Test delete product view if not a superuser '''

        self.client.login(
            username="testuser", password="testpassword")
        response = self.client.get(self.delete_product)
        self.assertRedirects(response, self.home)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Sorry, only store owners can do that.")

    def test_delete_post_GET_if_superuser(self):
        ''' Test delete product view if a superuser '''

        self.client.login(
            username="testadmin", password="testadminpassword")
        response = self.client.get(self.delete_product)
        self.assertRedirects(response, self.products)
        self.assertEqual(response.status_code, 302)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Product deleted!")

    def test_delete_product_POST(self):
        ''' Test the delete post post POST function '''

        self.client.login(
            username="testadmin", password="testadminpassword")
        response = self.client.post(self.delete_product)
        product = Product.objects.filter(id=self.product.id)
        self.assertFalse(product)
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Product deleted!")
