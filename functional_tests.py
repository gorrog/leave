from selenium import webdriver
import unittest

class BobVisitorTest(unittest.TestCase):

    def setUp(self):
        self.browser = webdriver.Firefox()

    def tearDown(self):
        self.browser.quit()

    def test_bob_can_log_in(self):
        # Bob would like to see how much leave he has available. He remembers
        # being informed that there is a company app for that.

        # He navigates to the app URL that his company provided for him, and
        # after some rummaging, finds the username and password he wrote down
        # for his user account.
        self.browser.get("http://localhost:8000")

        # He sees that the app mentions 'Leave' and 'Log in' in the title.
        self.assertIn("Leave", self.browser.title)
        self.assertIn("Log In", self.browser.title)

        # He sees that there is a form for logging on.
        login_legend = self.browser.find_element_by_css_selector(
            "#login_form fieldset legend"
        )
        self.assertEqual(login_legend.text, "Log In")

        # He clicks in the first field he sees.
        self.fail("Finish the test")

        # He sees that the field mentions his username.

        # He enters his real name (not his username)

        # He then hits enter (Bob is a little slow).

        # He is informed that he didn't enter his password.

        # He clicks in the password field and enters his password incorrectly.

        # He clicks the 'login' button.

        # He is informed that either his username or password is incorrect.

        # Bob realises that he entered his name instead of his username. He
        # corrects this.

        # He hits enter.

        # He is informed that either his username or password is incorrect.

        # Bob corrects his password and hits Enter.

        # He is taken to a new page that has a title "Bob's Leave"

        # On the top of the page he sees a link to Log off, so he knows he has
        # logged on successfully.

        # On the page Bob can see how many days he has remaining in 2016

        # Bob didn't take any leave the previous year so he has 5 days in
        # addition to his 18 allowed for this year (23 in total). Bob remembers
        # that he took 10 days off early in the year. He is happy to see that
        # the system has correctly calculated that he still has 13 days
        # remaining.

        # Bob wants to go on a 2 week (14 day) holiday in December. He decides
        # to log a leave request.

        # He looks around and sees that there is a section titled 'log a leave
        # request'

        # The section has fields for a start date, end date and a button with
        # the label 'log request'

        # Bob enters the start date as December 1st, 2016

        # Bob enters the end date as December 20th, 2016

        # Bob clicks the 'log request' button.

        # Bob is informed that this leave request is invalid. Bob realises that
        # he has selected 14 days, but only has 13 available. Knowing that 13
        # days is not enough for a decent holiday, Bob decides to extend his
        # holiday to 21 days spanning December 2016 and January 2017 so that he
        # can use some of next year's leave allowance. Bob selects December
        # 22nd, 2016 as the start date.  This leaves him with 6 unused days in
        # 2016 (13 available, minus 7 working days from 22/12 to 31/12.

        # He then selects Jan 19th 2017 as the end date.

        # He presses Enter

        # The page refreshes and Bob is shown a message saying that his leave
        # request is valid, but needs to be approved.

        # Bob notices that the page is now showing that he has 6 remaining days
        # in 2016

        # Bob wonders how many days he has left in 2017. He sees there is a
        # year picker at the top of the page.

        # He selects 2017 and hits enter.

        # The page refreshes and he is now shown his available leave for 2017.
        # Bob does some calculations and is satisfied that the system has
        # correctly calculated that he has 9 days remaining (18 standard days
        # plus maximum 5 carried over from 2016 = 23 - 14 days leave taken from
        # Jan 1-19 2017)

        # Bob is curious how much leave he would have in 2018. He selects 2018
        # from the year selector at the top of the page and then presses the
        # 'update' button.

        # The page refreshes and Bob notices that the title also mentions the
        # year.

        # Bob sees that he has 23 days of leave remaining for 2018.

        # Having done all that he wanted to, Bob clicks the "Log Off" link.

        # The page refreshes and the original page mentioning "Log On" is
        # shown.

        # Later, another user, Greg, decides to check how much leave he took in
        # 2015, using the same computer that Greg was previously using.

        # He opens the URL and makes sure that the title mentions 'Leave' and
        # 'Log In'.

        # He correctly inputs his username and password the first time (he is
        # more on-the-ball than Bob).

        # He presses the button that says "Log In"

        # The page refreshes. Greg is concerned that he might see Bob's leave
        # (since he was using the computer previously), but is relieved that
        # the page title mentions "Greg's Leave".

        # Greg chooses 2015 from the year picker and clicks the "Update"
        # button.

        # The page refreshes and now mentions 2015. Greg started in 2015 and
        # only remembered taking 5 days leave, so by his calculations, he
        # should have had 13 days left at the end of 2015.

        # After a discussion with his HR. manager, Greg decides to put in a
        # leave request for 5 days in July. He tries to select the start date
        # as 5 July, not realising that the year 2015 is selected. His is
        # unable to select the value.  Then he realises that he is on the wrong
        # year.

        # Greg then selects July 15 2016 as the start date.

        # He mistakenly selects July 10th as the end date.

        # He presses Enter

        # The system informs him that the end date must be after the start
        # date.

        # Greg corrects the error and hits Enter

        # The page updates and a message is shown to him telling him that his
        # leave date is valid, but needs to be approved first.

        # Greg notices that his available leave for 2016 has reduced from 23
        # days to 18 days.

        # Satisfied, he clicks the "Log off" link at the top of the page.

        # The page refreshes and the original page mentioning "Log On" is
        # shown.

if __name__ == '__main__':
    unittest.main()
