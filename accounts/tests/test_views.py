from django.test import TestCase
from django.urls import reverse
from accounts.models import Author
from django.contrib.auth import get_user_model
from blog.models import Blog, Comment
from django.contrib import messages
from django.contrib.auth.models import Group, Permission

class UserAuthTests(TestCase):

  def setUp(self):

    self.user = Author.objects.create_user(
      email='testuser@gmail.com',
      password='password123',
      username='abcdefghi',
      date_of_birth='2002-12-30',
      first_name='John',
      last_name='Doe',
      gender='Male',
      state='California',
      city='Los Angeles',
    )

    self.blog = Blog.objects.create(
      title="Test Blog", 
      content="This is a test blog", 
      author=self.user
    )

    self.valid_data = {
      'username': 'testuser',
      'email': 'testuser@example.com',
      'password1': 'password123',
      'password2': 'password123',
      'first_name': 'John',
      'last_name': 'Doe',
      'date_of_birth': '1990-01-01',
      'gender': 'Male',
      'state': 'California',
      'city': 'Los Angeles'
    }

    self.invalid_data = {
      'username': 'testuser',
      'email': 'invalidemail',  # Invalid email
      'password1': 'password123',
      'password2': 'password321',  # Mismatched passwords
      'first_name': 'John',
      'last_name': 'Doe',
      'date_of_birth': '1990-01-01',
      'gender': 'Male',
      'state': 'California',
      'city': 'Los Angeles'
    }


    self.group = Group.objects.create(name='admin')

    # Assign permissions to the group
    self.add_permissions_to_group(self.group, ['add_blog', 'change_blog', 'delete_blog'])
    self.user.groups.add(self.group)


    self.profile_url = reverse('profile')
    self.logout_url = reverse('logout')
    self.login_url = reverse('login')
    self.signup_url = reverse('signup')


  def test_custom_login_view(self):
    response = self.client.get('/accounts/login/')
    self.assertEqual(response.status_code, 200)


  def test_custom_login_view_valid_credentials(self):
    response = self.client.post(self.login_url, {'username':'testuser@gmail.com', 'password': 'password123'})
    self.assertRedirects(response, reverse('home'))
    self.assertEqual(response.status_code, 302)


  def test_custom_login_view_invalid_credentials(self):
    response = self.client.post(self.login_url, {'username':'testuser@gmail.com', 'password': 'wrongpassword'})
    self.assertContains(response, 'Your username and password didn\'t match. Please try again.')
    self.assertEqual(response.status_code, 200)


  def test_profile(self):
    self.test_custom_login_view_valid_credentials()
    response = self.client.get(self.profile_url)
    self.assertEqual(response.status_code, 200)
    self.assertContains(response, 'Test Blog')
    self.assertContains(response, 'This is a test blog')
    self.assertContains(response, 'testuser')
    self.assertContains(response, 'testuser@gmail.com')
    self.check_permission_in_response(response, 'add_blog', 'user_can_add_blog')
    self.check_permission_in_response(response, 'change_blog', 'user_can_change_blog')
    self.check_permission_in_response(response, 'delete_blog', 'user_can_delete_blog')   


  def test_profile_view_not_logged_in(self):
    response = self.client.get(self.profile_url)
    self.assertRedirects(response, f'{self.login_url}?next={self.profile_url}')


  def test_custom_logout_view(self):
    self.test_custom_login_view_valid_credentials()

    response = self.client.post(self.logout_url)
    self.assertRedirects(response, self.login_url)

    messages_list = list(response.wsgi_request._messages)
    message = messages_list[-1]  # Get the last message (which should be the logout message)
    self.assertEqual(message.message, "You have successfully logged out.")
    self.assertEqual(message.level, messages.INFO)

    response = self.client.get(reverse('profile'))
    self.assertRedirects(response, f"{self.login_url}?next={reverse('profile')}")


# ================ Helper methods ====================

  def add_permissions_to_group(self, group, permissions_codename):
    """Helper method to add multiple permissions to a group."""

    permissions = Permission.objects.filter(codename__in=permissions_codename)
    group.permissions.add(*permissions)


  def check_permission_in_response(self, response, permission_codename, context_key):
    """Helper method to check if a permission is in the response context."""

    if self.user.has_perm(f'blog.{permission_codename}'):
      self.assertIn(context_key, response.context)

    else:
      self.assertNotIn(context_key, response.context)