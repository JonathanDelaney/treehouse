from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.messages import get_messages
from profiles.forms import UserProfileForm
from profiles.models import UserProfile
from checkout.models import Order


class TestUserViews(TestCase):
    def setUp(self):
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@email.com',
            password='testpassword'
        )
        self.profile = reverse("profile")
        self.login = reverse("account_login")
        self.form = UserProfileForm

    def test_profile_login_required(self):
        ''' Test the user needs to be logged in to see the userprofile page '''

        response = self.client.get(self.profile)
        self.assertNotEqual(response.status_code, 200)

    def test_profile_page_logged_in(self):
        ''' Test the user profile page when logged in '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.get(self.profile)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "profiles/profile.html")
        self.assertTemplateUsed(response, "base.html")

    def test_profile_post_error(self):
        ''' Test if form filled out incorrectly '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.profile, {
            "default_postcode": "0808876567889998765543345677"}
        )
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Update failed. Please ensure the form is valid.")

    def test_profile_post_valid_form(self):
        ''' Test if from is valid '''

        self.client.login(username="testuser", password="testpassword")
        response = self.client.post(self.profile, {
            'default_phone_number': '1234567890',
            'default_postcode': 'd22 h123',
            'default_town_or_city': 'Dublin',
            'default_street_address1': '123 Fade st',
            'default_street_address2': 'Georges st',
            'default_county': 'Co Dublin'}
        )
        form = self.form(response, instance=self.user)
        self.assertTrue(form.is_valid())
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         "Profile updated successfully")

    def test_order_history_view_unloggedin(self):
        ''' Test view of previous orders not logged in '''

        profile = UserProfile.objects.get(user=self.user)
        order = Order.objects.create(user_profile=profile)
        response = self.client.get(
            reverse("order_history",
                    kwargs={"order_number": order.order_number}))
        self.assertEqual(response.status_code, 200)

    def test_order_history_view(self):
        ''' Test previous orders view with logged in user '''

        self.client.login(username="testuser", password="testpassword")
        profile = UserProfile.objects.get(user=self.user)

        order = Order.objects.create(user_profile=profile)

        response = self.client.get(
            reverse("order_history",
                    kwargs={"order_number": order.order_number}))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "checkout/checkout_success.html")
        self.assertTemplateUsed(response, "base.html")
        messages = list(get_messages(response.wsgi_request))
        self.assertEqual(len(messages), 1)
        self.assertEqual(str(messages[0]),
                         f'This is a past confirmation for order number \
                            {order}. \
                            A confirmation email was sent on the order date.')
