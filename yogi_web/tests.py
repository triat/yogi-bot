from django.test import TestCase

from .views import return_one


class FakeTest(TestCase):

    def test_return_one(self):
        self.assertEqual(return_one(), 1)
