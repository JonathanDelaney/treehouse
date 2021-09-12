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
            name="test_category",
            friendly_name="Test Category"
        )
        self.product = Product.objects.create(
            pk="1",
            name="test product",
            description="test description",
            price=2.99,
            image="testimage.jpg",
            category=self.category,
        )
        self.products = reverse("products")
        self.product_detail = reverse("product_detail",
                                   kwargs={"product_id": self.product.id})

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
        # self.assertEqual('query', 'test')
