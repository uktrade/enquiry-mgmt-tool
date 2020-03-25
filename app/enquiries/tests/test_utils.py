import app.enquiries.tests.utils as test_utils


class UtilsTestCase(test_utils.BaseEnquiryTestCase):
    def test_helper_logout(self):
        """
        Tests that the `self.logged` property is correctly set when logging in/out
        """
        self.login()
        self.assertEqual(self.logged_in, True)
        self.logout()
        self.assertEqual(self.logged_in, False)
        # re-authenticate so subsequent tests can pass
        self.login()
