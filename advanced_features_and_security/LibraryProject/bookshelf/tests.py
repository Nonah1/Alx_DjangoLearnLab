from django.test import TestCase
from .forms import ExampleForm

class ExampleFormTest(TestCase):
    def test_example_form_valid_data(self):
        form = ExampleForm(data={
            'title': 'Test Book',
            'author': 'John Doe',
            'published_year': 2023
        })
        self.assertTrue(form.is_valid())

    def test_example_form_missing_data(self):
        form = ExampleForm(data={})
        self.assertFalse(form.is_valid())
        self.assertIn('title', form.errors)
        self.assertIn('author', form.errors)
        self.assertIn('published_year', form.errors)
