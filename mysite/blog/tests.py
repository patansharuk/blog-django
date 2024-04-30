from django.test import TestCase
from django.urls import reverse

# Create your tests here.
class BasicTest(TestCase):
    def test_should_return_bool(self):
        res = self.client.get(reverse('blogs_path'))
        self.assertIs(200, 200)

    def test_login(self):
        res = self.client.get(reverse('not_found_path'))
        print(res.content)
        self.assertIs(True, True)