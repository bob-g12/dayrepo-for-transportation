from django.test import TestCase
from django.http import HttpRequest
from snippets.views import top

# Create your tests here.
class TopPageViewTest(TestCase):
    def test_top_returns_200(self):
        request = HttpRequest()

        res = top(request)
        self.assertEqual(res.status_code, 200)
