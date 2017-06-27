from django.test import TestCase


class BaseTest(TestCase):
    # here we do any initialisation for tests that can be global
    # e.g. setup db fixtures, fire servers etc.

    def setUp(self):
        pass
