from django.urls import resolve
from django.test import TestCase

from leave.views import login_page

class LoginPageTest(TestCase):

    def test_root_url_resolves_to_login_page_view(self):
        found = resolve('/')
        self.assertEqual(found.func, login_page)
