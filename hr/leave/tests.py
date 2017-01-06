from django.test import LiveServerTestCase
from django.http import HttpRequest
from django.template.loader import render_to_string
from django.contrib.auth.models import AnonymousUser
from django.contrib.auth import authenticate
from django.contrib.sessions.models import Session

from datetime import datetime


from leave.views import login_page, home_page

from leave.models import Employee, Leave

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
        Employee.objects.create_user("Bobby12", password = "Bobobo1234",
                start_date="2015-01-01")
        post_data = {
                "username": "Bobby12",
                "password": "Bobobo1234"
                }
        response = self.client.post("/login/",post_data)
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/')

class LogoutTest(LiveServerTestCase):

    def setUp(self):
        username = "Bobby12"
        password = "Bobobo1234"
        start_date = "2015-01-01"
        Employee.objects.create_user(username=username, password=password,
                start_date=start_date)
        self.user = authenticate(username=username, password=password)
        self.client.login(username=username, password=password)


    def tearDown(self):
        pass

    def test_get_request_to_logout_returns_bad_request_error(self):
        response = self.client.get("/logout/")
        self.assertEqual(response.status_code, 400)

    def test_logout_link_removes_session_data(self):
        session_objects = Session.objects.all()
        number_of_sessions = len(session_objects)
        self.assertTrue(number_of_sessions == 1)
        self.client.post("/logout/")
        session_objects = Session.objects.all()
        number_of_sessions = len(session_objects)
        self.assertTrue(number_of_sessions == 0)

    def test_logout_link_redirects_to_login(self):
        response = self.client.post("/logout/")
        self.assertEqual(response.status_code, 302)
        self.assertEqual(response.url, '/login/')

class HomePageTest(LiveServerTestCase):
    def setUp(self):
        username = "Bobby12"
        password = "Bobobo1234"
        start_date = "2015-01-01"
        Employee.objects.create_user(username=username, password=password,
                start_date=start_date)
        self.user = authenticate(username=username, password=password)
        self.client.login(username=username, password=password)

    def tearDown(self):
        pass

    def test_no_arguments_request_to_home_page_returns_current_year(self):
        response = self.client.get("/")
        current_year = datetime.strftime(datetime.now(), "%Y")
        self.assertContains(response, current_year)

class EmployeeModelTest(LiveServerTestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_saving_and_recalling_items(self):
        first_employee = Employee()
        first_employee.start_date = "2015-02-13"
        first_employee.username = "Jackie1"
        first_employee.save()

        second_employee = Employee()
        second_employee.start_date = "2013-08-03"
        first_employee.username = "Jackie2"
        second_employee.save()

        saved_items = Employee.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_retrieved_employee = saved_items[0]
        first_start_date = str(first_retrieved_employee.start_date)
        self.assertEqual(first_start_date, "2015-02-13")

        second_retrieved_employee = saved_items[1]
        second_start_date = str(second_retrieved_employee.start_date)
        self.assertEqual(second_start_date, "2013-08-03")

    def test_calculated_fields_correct(self):
        first_employee = Employee()
        first_employee.start_date = "2015-02-13"
        first_employee.username = "Jackie1"
        first_employee.save()

        second_employee = Employee()
        second_employee.start_date = "2013-08-03"
        first_employee.username = "Jackie2"
        second_employee.save()

        saved_items = Employee.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_retrieved_employee = saved_items[0]
        self.assertEqual(first_retrieved_employee.leave_remaining, 23)

        second_retrieved_employee = saved_items[1]
        self.assertEqual(second_retrieved_employee.leave_remaining, 23)

class LeaveModelTest(LiveServerTestCase):
    def setUp(self):
        self.first_employee = Employee()
        self.first_employee.start_date = "2015-02-13"
        self.first_employee.username = "Jackie1"
        self.first_employee.save()

        self.second_employee = Employee()
        self.second_employee.start_date = "2013-08-03"
        self.second_employee.username = "Jackie2"
        self.second_employee.save()

    def test_saving_and_recalling_items(self):
        first_leave = Leave()
        first_leave.start_date = "2013-03-28"
        first_leave.end_date = "2013-04-05"
        first_leave.status = "approved"
        first_leave.employee = self.first_employee
        first_leave.save()

        second_leave = Leave()
        second_leave.start_date = "2014-05-08"
        second_leave.end_date = "2014-05-15"
        second_leave.status = "declined"
        # We use the first employee for both leave objects
        second_leave.employee = self.first_employee
        second_leave.save()

        saved_items = Leave.objects.all()
        self.assertEqual(saved_items.count(), 2)

        first_retrieved_leave = saved_items[0]
        first_start_date = str(first_retrieved_leave.start_date)
        self.assertEqual(first_start_date, "2013-03-28")
        self.assertEqual(first_retrieved_leave.employee, self.first_employee)
        self.assertEqual(first_retrieved_leave.working_days_in_leave_period, 7)

        second_retrieved_leave = saved_items[1]
        second_start_date = str(second_retrieved_leave.start_date)
        self.assertEqual(second_start_date, "2014-05-08")
        self.assertEqual(second_retrieved_leave.employee, self.first_employee)
        self.assertEqual(second_retrieved_leave.working_days_in_leave_period, 6)
