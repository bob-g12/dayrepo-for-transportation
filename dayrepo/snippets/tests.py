from django.test import TestCase
from django.http import HttpRequest
from snippets.views import top, snippet_new, snippet_new_checklist, snippet_update, snippet_update_checklist, pre_car_registration, car_registration, get_employee
from django.urls import resolve

# Create your tests here.
class SnippetTopViewTest(TestCase):
    def test_top_returns_200(self):
        res = self.client.get("/") 
        self.assertEqual(res.status_code, 200)
    
    def test_should_resolve_snippet_top(self):
        found = resolve("/")
        self.assertEqual(top, found.func)

class SnippetNewTest(TestCase):
    def test_should_resolve_snippet_new(self):
        found = resolve("/snippets/new/")
        self.assertEqual(snippet_new, found.func)

class SnippetNewChecklistTest(TestCase):
    def test_should_resolve_snippet_new_checklist(self):
        found = resolve("/snippets/new/checklist")
        self.assertEqual(snippet_new_checklist, found.func)

class SnippetUpdateTest(TestCase):
    def test_should_resolve_snippet_update(self):
        found = resolve("/snippets/1/")
        self.assertEqual(snippet_update, found.func)

class SnippetUpdateChecklistTest(TestCase):
    def test_should_resolve_snippet_update_checklist(self):
        found = resolve("/snippets/1/checklist/")
        self.assertEqual(snippet_update_checklist, found.func)

class PreCarRegistrationTest(TestCase):
    def test_should_resolve_pre_car_registration(self):
        found = resolve("/snippets/car/")
        self.assertEqual(pre_car_registration, found.func)

class CarRegistrationTest(TestCase):
    def test_should_resolve_car_registration(self):
        found = resolve("/snippets/car/new/")
        self.assertEqual(car_registration, found.func)

class GetEmployeeTest(TestCase):
    def test_should_resolve_car_registration(self):
        found = resolve("/snippets/employee/")
        self.assertEqual(get_employee, found.func)