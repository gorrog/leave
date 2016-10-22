from django.test import LiveServerTestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import User, AnonymousUser

from leave.views import login_page, home_page

class LoginPageTest(LiveServerTestCase):

    def setUp(self):
        pass

    def tearDown(self):
        pass


    def test_home_view_redirects_to_login_page_for_unauthenticated_user(self):
        request = HttpRequest()
        # These 2 lines below are needed for the @login_required decorator.
        # This took me hours to figure out. GRRRR!
        request.META['SERVER_NAME']="localhost"
        request.META['SERVER_PORT']="8000"

        anonymous_user = AnonymousUser()
        request.__setattr__("user",anonymous_user)
        response = home_page(request)
        self.assertTrue(response.status_code == 302)
        self.assertEqual(
                response.__getitem__("location"),
                "/login/?next="
                )

    def test_login_page_returns_correct_html(self):
        request = HttpRequest()
        response = login_page(request)
        expected_html = render_to_string('login.html', request=request)
        self.assertIn("Log In",expected_html)
        self.assertIn("Log In",response.content.decode())

    def test_missing_or_empty_password_returns_to_login_page(self):
        response = self.client.post('/login/',{"username": "some_name"})
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Log In", status_code=200)
        post_data = {
                "username": "some_name",
                "password": ""
                }
        response = self.client.post("/login/",post_data)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Log In", status_code=200)

    def test_missing_or_empty_username_returns_to_login_page(self):
        response = self.client.post('/login/',{"password": "some_name"})
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Log In", status_code=200)
        post_data = {
                "username": "",
                "password": "hello"
                }
        response = self.client.post("/login/",post_data)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Log In", status_code=200)

    def test_missing_or_empty_password_returns_error(self):
        response = self.client.post('/login/',{"username": "some_name"})
        self.assertContains(response,"Password was missing")
        post_data = {
                "username": "some_name",
                "password": ""
                }
        response = self.client.post("/login/",post_data)
        self.assertContains(response,"Password was missing")

    def test_missing_or_empty_username_returns_error(self):
        response = self.client.post('/login/',{"password": "blah"})
        self.assertContains(response,"Username was missing")
        post_data = {
                "username": "",
                "password": "blah"
                }
        response = self.client.post("/login/",post_data)
        self.assertContains(response,"Username was missing")

    def test_wrong_credentials_returns_to_login_page(self):
        post_data = {
                "username": "some_name",
                "password": "blahdeeblah"
                }
        response = self.client.post("/login/",post_data)
        self.assertTemplateUsed(response, 'login.html')
        self.assertContains(response, "Log In", status_code=200)

    def test_correct_credentials_redirects_to_home_page_view(self):
        User.objects.create_user("Bobby12", password = "Bobobo1234")
        post_data = {
                "username": "Bobby12",
                "password": "Bobobo1234"
                }
        response = self.client.post("/login/",post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

