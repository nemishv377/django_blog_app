from django.test import TestCase
from accounts.models import Author
from django.contrib.auth import get_user_model
from django.utils import timezone
from django.contrib.auth.hashers import check_password
from django.core.exceptions import ValidationError

# Create your tests here.

class AuthorModelTestBase(TestCase):
  
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


class AuthorTestCase(AuthorModelTestBase):

  def test_author_str_method(self):
    self.assertEqual(str(self.user), self.user.username)


  def test_author_create_user(self):  
    self._check_author_fields(self.user, self.user_data)


  def test_author_create_superuser(self):
    self._check_author_fields(self.superuser, self.superuser_data)
    self.assertTrue(self.superuser.is_staff)
    self.assertTrue(self.superuser.is_superuser)
    
  
  def test_author_field_labels_and_lengths(self):
    
    # Check that title has the expected label
    self.assertEqual(self.user._meta.get_field('email').verbose_name, 'email')
    self.assertEqual(self.user._meta.get_field('first_name').verbose_name, 'first name')
    self.assertEqual(self.user._meta.get_field('last_name').verbose_name, 'last name')
    self.assertEqual(self.user._meta.get_field('joining_date').verbose_name, 'joining date')
    self.assertEqual(self.user._meta.get_field('gender').verbose_name, 'gender')
    self.assertEqual(self.user._meta.get_field('date_of_birth').verbose_name, 'date of birth')
    self.assertEqual(self.user._meta.get_field('state').verbose_name, 'state')
    self.assertEqual(self.user._meta.get_field('city').verbose_name, 'city')
    
    # Check that fields are not null (required fields)
    self.assertFalse(self.user._meta.get_field('email').null)
    self.assertFalse(self.user._meta.get_field('first_name').null)
    self.assertFalse(self.user._meta.get_field('last_name').null)
    self.assertFalse(self.user._meta.get_field('joining_date').null)
    self.assertFalse(self.user._meta.get_field('gender').null)
    self.assertFalse(self.user._meta.get_field('date_of_birth').null)
    self.assertFalse(self.user._meta.get_field('state').null)
    self.assertFalse(self.user._meta.get_field('city').null)
        
    # Check max lengths
    self.assertEqual(self.user._meta.get_field('first_name').max_length, 30)
    self.assertEqual(self.user._meta.get_field('last_name').max_length, 30)
    self.assertEqual(self.user._meta.get_field('state').max_length, 30)
    self.assertEqual(self.user._meta.get_field('city').max_length, 30)
    self.assertEqual(self.user._meta.get_field('gender').max_length, 20)
    
    # Check gender choices
    gender_choices = dict(Author.GENDER_CHOICES)
    self.assertIn('Male', gender_choices)
    self.assertIn('Female', gender_choices)
    self.assertIn('Other', gender_choices)

    self._check_duplicate_field('email', "testuser@example.com", "anotheruser")
    self._check_duplicate_field('username', "anotheruser@example.com", "testuser")
    

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
    
  
  def _check_duplicate_field(self, field_name, email, username):
    """Helper method to check if a field raises a ValidationError for duplicates."""
    
    # Create a duplicate author instance with the same field value
    author_duplicate = Author(
      email=email if field_name == 'email' else "anotheruser@example.com",  # Set the duplicate email or username
      username=username if field_name == 'username' else "anotheruser",  # Set the other value
      password='password123',
      first_name="Jane",
      last_name="Smith",
      gender="Female",
      date_of_birth="1995-02-02",
      state="Texas",
      city="Dallas",
    )
    
    # Should raise a ValidationError due to duplicate value
    try:
      author_duplicate.full_clean()
    
    except ValidationError as e:
      self.assertIn(field_name, e.message_dict)  # Ensure the error message is related to the given field
    
    else:
      self.fail(f"Expected ValidationError due to duplicate {field_name}, but it was not raised.")