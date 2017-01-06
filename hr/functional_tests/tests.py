from django.test import LiveServerTestCase
from leave.models import Employee
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from time import sleep
from datetime import datetime

class BobVisitorTest(LiveServerTestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()
        self.browser.implicitly_wait(3)

    def tearDown(self):
        self.browser.quit()

    def test_login_form_working(self):
        # Bob would like to see how much leave he has available. He remembers
        # being informed that there is a company app for that.

        # He navigates to the app URL that his company provided for him, and
        # after some rummaging, finds the username and password he wrote down
        # for his user account.
        self.browser.get(self.live_server_url)

        # Because Bob isn't logged in, he is automatically redirected to the
        # login URL
        self.assertIn("login", self.browser.current_url)

        # He sees that the app mentions 'Leave' and 'Log in' in the title.
        self.assertIn("Leave", self.browser.title)
        self.assertIn("Log In", self.browser.title)

        # He sees that there is a form for logging on.
        login_legend = self.browser.find_element_by_css_selector(
            "#login_form fieldset legend"
        )
        self.assertEqual(login_legend.text, "Log In")

        # He clicks in the first field he sees.
        username_input = self.browser.find_element_by_css_selector(
                "input.username"
                )
        username_input.click()

        # He sees that the field mentions his username.
        username_label = self.browser.find_element_by_css_selector(
                "label.username"
                )
        self.assertIn("User Name", username_label.text)

        # He enters his real name (not his username)
        username_input.send_keys("Bob")

        # He then hits enter (Bob is a little slow).
        username_input.send_keys(Keys.ENTER)


        # He is informed that he didn't enter his password.
        error_message = self.browser.find_element_by_css_selector(
                "section#error p"
                )
        self.assertIn("Password was missing or empty", error_message.text)

        # He clicks in the password field and enters his password.
        # Bob doesn't realise that the page has refreshed and his username has
        # been cleared.
        password_input = self.browser.find_element_by_css_selector(
                "input.password"
                )
        password_input.send_keys("Bobobo123")

        # He clicks the 'login' button.
        login_button = self.browser.find_element_by_css_selector(
                "input#login_form_button"
                )
        login_button.click()

        ## This appears to be necessary to make Selenium wait for the browser
        ## to update.
        sleep(1)

        # He is informed that he didn't enter his password.
        error_message = self.browser.find_element_by_css_selector(
                "section#error p"
                )
        self.assertIn("Username was missing or empty", error_message.text)

        # Realising that he is having a very bad day, Bob enters his username
        # and password, but makes a mistake with his password
        username_input = self.browser.find_element_by_css_selector(
                "input.username"
                )
        username_input.send_keys("Bobby12")
        password_input = self.browser.find_element_by_css_selector(
                "input.password"
                )
        password_input.send_keys("Bobobo123")

        # He clicks the 'login' button.
        login_button = self.browser.find_element_by_css_selector(
                "input#login_form_button"
                )
        login_button.click()

        ## This appears to be necessary to make Selenium wait for the browser
        ## to update.
        sleep(1)

        # He is informed that either his username or password is incorrect.
        error_message = self.browser.find_element_by_css_selector(
                "section#error p"
                )
        self.assertIn("Username or Password was incorrect. Please try again",
                error_message.text)


    def test_bob_can_log_in_and_out(self):
        Employee.objects.create_user(username="Bobby12", password =
                "Bobobo1234", email="bob@example.com", start_date="2015-01-01")
        self.browser.get(self.live_server_url)
        # Bob fixes the problem and now finally enters the correct username and
        # password.
        username_input = self.browser.find_element_by_css_selector(
                "input.username"
                )
        username_input.send_keys("Bobby12")
        password_input = self.browser.find_element_by_css_selector(
                "input.password"
                )
        password_input.send_keys("Bobobo1234")

        # He hits enter.
        password_input.send_keys(Keys.ENTER)

        ## This appears to be necessary to make Selenium wait for the browser
        ## to update.
        sleep(1)

        # He is taken to a new page that has a title "Bobby12's Leave"
        home_page_title = self.browser.find_element_by_css_selector(
                "section#main_content h1"
                )
        self.assertIn("Bobby12's Leave", home_page_title.text)

        # On the top of the page he sees a button to Log off, so he knows he
        # has logged on successfully.
        logout_button = self.browser.find_element_by_css_selector(
                "input#logout"
                )
        self.assertIn("Log Out", logout_button.get_attribute("value"))

        # Bob accidentally clicks the link!
        logout_button.click()

        ## This appears to be necessary to make Selenium wait for the browser
        ## to update.
        sleep(1)

        # Unfortunately, in response, the system logs Bob off and he is taken
        # back to the login page
        self.assertIn("Log In", self.browser.title)

        # Undeterred, Bob enters his username and password and hits Enter.
        # Amazingly, he makes no mistakes this time
        username_input = self.browser.find_element_by_css_selector(
                "input.username"
                )
        username_input.send_keys("Bobby12")
        password_input = self.browser.find_element_by_css_selector(
                "input.password"
                )
        password_input.send_keys("Bobobo1234")
        password_input.send_keys(Keys.ENTER)

        # He is successfully logged in. Bob knows this because he can see the
        # 'log off' button. He makes a mental note not to click that again 
        # until he wants to log off.
        logout_button = self.browser.find_element_by_css_selector(
                "input#logout"
                )
        self.assertIn("Log Out", logout_button.get_attribute("value"))

        ## This appears to be necessary to make Selenium wait for the browser
        ## to update.
        sleep(5)

        # On the page Bob can see how many leave days he has remaining in the
        # current year
        selected_year = self.browser.find_element_by_id("selected_year")
        current_year = datetime.strftime(datetime.now(), "%Y")
        self.assertEqual(selected_year.text, current_year)
        days_remaining = self.browser.find_element_by_id("days_remaining")
        self.assertTrue(str.isdigit(days_remaining.text))


        # Bob didn't take any leave the previous year so he has 5 days in
        # addition to his 18 allowed for this year (23 in total). Bob remembers
        # that he took 10 days off early in the year. He is happy to see that
        # the system has correctly calculated that he still has 13 days
        # remaining.
        self.fail("Finish the test")

        # Bob wants to go on a 2 week (14 day) holiday in December. He decides
        # to log a leave request.
        self.fail("Finish the test")

        # He looks around and sees that there is a section titled 'log a leave
        # request'
        self.fail("Finish the test")

        # The section has fields for a start date, end date and a button with
        # the label 'log request'
        self.fail("Finish the test")

        # Bob enters the start date as December 1st, 2016
        self.fail("Finish the test")

        # Bob enters the end date as December 20th, 2016
        self.fail("Finish the test")

        # Bob clicks the 'log request' button.
        self.fail("Finish the test")

        # Bob is informed that this leave request is invalid. Bob realises that
        # he has selected 14 days, but only has 13 available. Knowing that 13
        # days is not enough for a decent holiday, Bob decides to extend his
        # holiday to 21 days spanning December 2016 and January 2017 so that he
        # can use some of next year's leave allowance. Bob selects December
        # 22nd, 2016 as the start date.  This leaves him with 6 unused days in
        # 2016 (13 available, minus 7 working days from 22/12 to 31/12.
        self.fail("Finish the test")

        # He then selects Jan 19th 2017 as the end date.
        self.fail("Finish the test")

        # He presses Enter
        self.fail("Finish the test")

        # The page refreshes and Bob is shown a message saying that his leave
        # request is valid, but needs to be approved.
        self.fail("Finish the test")

        # Bob notices that the page is now showing that he has 6 remaining days
        # in 2016
        self.fail("Finish the test")

        # Bob wonders how many days he has left in 2017. He sees there is a
        # year picker at the top of the page.
        self.fail("Finish the test")

        # He selects 2017 and hits enter.
        self.fail("Finish the test")

        # The page refreshes and he is now shown his available leave for 2017.
        # Bob does some calculations and is satisfied that the system has
        # correctly calculated that he has 9 days remaining (18 standard days
        # plus maximum 5 carried over from 2016 = 23 - 14 days leave taken from
        # Jan 1-19 2017)
        self.fail("Finish the test")

        # Bob is curious how much leave he would have in 2018. He selects 2018
        # from the year selector at the top of the page and then presses the
        # 'update' button.
        self.fail("Finish the test")

        # The page refreshes and Bob notices that the title also mentions the
        # year.
        self.fail("Finish the test")

        # Bob sees that he has 23 days of leave remaining for 2018.
        self.fail("Finish the test")

        # Having done all that he wanted to, Bob clicks the "Log Out" link.
        self.fail("Finish the test")

        # The page refreshes and the original page mentioning "Log On" is
        # shown.
        self.fail("Finish the test")

        # Later, another user, Greg, decides to check how much leave he took in
        # 2015, using the same computer that Greg was previously using.
        self.fail("Finish the test")

        # He opens the URL and makes sure that the title mentions 'Leave' and
        # 'Log In'.
        self.fail("Finish the test")

        # He correctly inputs his username and password the first time (he is
        # more on-the-ball than Bob).
        self.fail("Finish the test")

        # He presses the button that says "Log In"
        self.fail("Finish the test")

        # The page refreshes. Greg is concerned that he might see Bob's leave
        # (since he was using the computer previously), but is relieved that
        # the page title mentions "Greg's Leave".
        self.fail("Finish the test")

        # Greg chooses 2015 from the year picker and clicks the "Update"
        # button.
        self.fail("Finish the test")

        # The page refreshes and now mentions 2015. Greg started in 2015 and
        # only remembered taking 5 days leave, so by his calculations, he
        # should have had 13 days left at the end of 2015.
        self.fail("Finish the test")

        # After a discussion with his HR. manager, Greg decides to put in a
        # leave request for 5 days in July. He tries to select the start date
        # as 5 July, not realising that the year 2015 is selected. His is
        # unable to select the value.  Then he realises that he is on the wrong
        # year.
        self.fail("Finish the test")

        # Greg then selects July 15 2016 as the start date.
        self.fail("Finish the test")

        # He mistakenly selects July 10th as the end date.
        self.fail("Finish the test")

        # He presses Enter
        self.fail("Finish the test")

        # The system informs him that the end date must be after the start
        # date.
        self.fail("Finish the test")

        # Greg corrects the error and hits Enter
        self.fail("Finish the test")

        # The page updates and a message is shown to him telling him that his
        # leave date is valid, but needs to be approved first.
        self.fail("Finish the test")

        # Greg notices that his available leave for 2016 has reduced from 23
        # days to 18 days.
        self.fail("Finish the test")

        # Satisfied, he clicks the "Log off" link at the top of the page.
        self.fail("Finish the test")

        # The page refreshes and the original page mentioning "Log On" is
        # shown.
        self.fail("Finish the test")
