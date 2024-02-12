from django.test import TestCase
from django.http import HttpRequest

# Create your tests here.
class TopPageViewTest(TestCase):
    def test_top_returns_200(self):
        request = HttpRequest()