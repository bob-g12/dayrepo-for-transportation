from django.test import TestCase
from django.http import HttpRequest
from snippets.views import top, snippet_new
from django.urls import resolve

# Create your tests here.
class SnippetTopViewTest(TestCase):
    def test_top_returns_200(self):
        res = self.client.get("/") 
        self.assertEqual(res.status_code, 200)
    
    def test_should_resolve_snippet_top(self):
        found = resolve("/")
        self.assertEqual(top, found.func)

class SnippetUpdateTest(TestCase):
    def test_should_resolve_snippet_new(self):
        found = resolve("/snippets/new/")
        self.assertEqual(snippet_new, found.func)
