from django.urls import resolve
from django.test import TestCase
from django.http import HttpRequest
from django.template.loader import render_to_string

from leave.views import login_page

class LoginPageTest(TestCase):

    def test_root_url_resolves_to_login_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, login_page)

    def test_login_page_returns_correct_html(self):
        request = HttpRequest()
        response = login_page(request)
        expected_html = render_to_string('login.html')
        print("response is: {}".format(response.content.decode()))
        print("expected_html is: {}".format(expected_html))
        self.assertEqual(response.content.decode(), expected_html)

