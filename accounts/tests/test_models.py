from django.test import TestCase
from accounts.models import Author
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.hashers import check_password

# Create your tests here.

class AuthorTestCase(TestCase):

  def setUp(self):
    """Set up any necessary objects for the tests."""
    # User test data
    self.user_data = {
      'email': 'testuser@example.com',
      'username': 'testuser',
      'first_name': 'John',
      'last_name': 'Doe',
      'gender': 'Male',
      'date_of_birth': '1990-01-01',
      'state': 'California',
      'city': 'Los Angeles',
      'password': 'password1234'
    }

    # Superuser test data
    self.superuser_data = {
      'email': 'superuser@example.com',
      'username': 'superuser',
      'first_name': 'Super',
      'last_name': 'User',
      'gender': 'Female',
      'date_of_birth': '1985-05-15',
      'state': 'New York',
      'city': 'New York City',
      'password': 'superpassword'
    }

    self.Author = get_user_model()
    self.user = self.Author.objects.create_user(**self.user_data)
    self.superuser = self.Author.objects.create_superuser(**self.superuser_data)


  def test_author_str_method(self):
    self.assertEqual(str(self.user), self.user.username)


  def test_author_create_user(self):  
    self._check_author_fields(self.user, self.user_data)


  def test_author_create_superuser(self):
    self._check_author_fields(self.superuser, self.superuser_data)
    self.assertTrue(self.superuser.is_staff)
    self.assertTrue(self.superuser.is_superuser)


  def _check_author_fields(self, author, data):
    self.assertEqual(author.email, data['email'])
    self.assertEqual(author.first_name, data['first_name'])
    self.assertEqual(author.last_name, data['last_name'])
    self.assertEqual(author.username, data['username'])
    self.assertEqual(author.gender, data['gender'])
    self.assertEqual(author.state, data['state'])
    self.assertEqual(author.city, data['city'])
    self.assertEqual(str(author.date_of_birth), data['date_of_birth'])
    self.assertTrue(author.joining_date <= timezone.now())
    self.assertTrue(check_password(data['password'], author.password))