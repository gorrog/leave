from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser

from leave.views import login_page, home_page

class LoginPageTest(TestCase):


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
        expected_html = render_to_string('login.html')
        self.assertEqual(response.content.decode(), expected_html)

    def test_missing_or_empty_password_returns_error(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST = {
                "username": "some_name"
                }
        response = login_page(request)
        self.assertIn( "missing password", response.content.decode)
        request = HttpRequest()
        request.method = "POST"
        request.POST = {
                "username": "some_name",
                "password": ""
                }
        response = login_page(request)
        self.assertIn( "missing password", response.content.decode)

    def test_missing_or_empty_password_redirects_to_login_page(self):
        request = HttpRequest()
        request.method = "POST"
        request.POST = {
                "username": "some_name"
                }
        response = login_page(request)
        self.assertTrue(response.status_code == 302)
        self.assertEqual(
                response.__getitem__("location"),
                "/login/?next="
                )
        request = HttpRequest()
        request.method = "POST"
        request.POST = {
                "username": "some_name",
                "password": ""
                }
        response = login_page(request)
        self.assertTrue(response.status_code == 302)
        self.assertEqual(
                response.__getitem__("location"),
                "/login/?next="
                )
