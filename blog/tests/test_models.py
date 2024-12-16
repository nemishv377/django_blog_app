from django.test import TestCase
from blog.models import Blog, Comment
from accounts.tests.test_models import AuthorModelTestBase
from django.core.files.uploadedfile import SimpleUploadedFile
from django.urls import reverse
from django.core.exceptions import ValidationError
import os


class BlogModelTestBase(AuthorModelTestBase):

  def setUp(self):

    super().setUp()
    self.Blog = Blog

    image_path = os.path.join(os.path.dirname(__file__), 'test_image.jpg')
    with open(image_path, 'wb') as f:
      f.write(b'fake image data')

    self.blog = self.Blog.objects.create(
      title="Test Blog", 
      content="Test content", 
      image=SimpleUploadedFile(name='test_image.jpg', content=b'fake image data', content_type='image/jpeg'),
      author=self.user
    )



class BlogModelTest(BlogModelTestBase):

  def test_blog_field_labels_and_lengths(self):

    # Check that title has the expected label
    self.assertEqual(self.blog._meta.get_field('title').verbose_name, 'title')
    self.assertEqual(self.blog._meta.get_field('content').verbose_name, 'content')
    self.assertEqual(self.blog._meta.get_field('image').verbose_name, 'image')
    self.assertEqual(self.blog._meta.get_field('author').verbose_name, 'author')
    self.assertEqual(self.blog._meta.get_field('title').max_length, 200)

    self.assertTrue(self.blog._meta.get_field('created_at').auto_now_add)
    self.assertTrue(self.blog._meta.get_field('updated_at').auto_now)
    
    # Check that fields are not null (required fields)
    self.assertFalse(self.blog._meta.get_field('title').null)
    self.assertFalse(self.blog._meta.get_field('content').null)
    self.assertFalse(self.blog._meta.get_field('image').null)
    self.assertFalse(self.blog._meta.get_field('author').null)
    self.assertFalse(self.blog._meta.get_field('created_at').null)
    self.assertFalse(self.blog._meta.get_field('updated_at').null)    
    

  def test_blog_str(self):
    self.assertEqual(str(self.blog), self.blog.title)


  def test_blog_get_absolute_url(self):
    expected_url = reverse('blog_detail', kwargs={'id': self.blog.id})
    self.assertEqual(self.blog.get_absolute_url(), expected_url)


  def test_image_size_validation(self):
    # Create a large image file (over 10MB)
    large_image_content = b"Fake image content" * 1024 * 1024  # 1MB * 10
    large_image = SimpleUploadedFile("large_image.jpg", large_image_content, content_type="image/jpeg")
    
    blog = Blog(
      title="Large Image Blog",
      content="This blog has a large image.",
      image=large_image,
      author=self.user
    )
    
    with self.assertRaises(ValidationError):
      blog.clean()  # This will trigger the clean method



class CommentModelTest(BlogModelTestBase):
  
  def setUp(self):
    
    super().setUp()
    self.Comment = Comment
    
    self.comment_1 = self.Comment.objects.create(
      blog=self.blog,
      author=self.user,
      message="This is the first test comment.",
    )
    
    self.comment_2 = self.Comment.objects.create(
      blog=self.blog,
      author=self.user,
      message="This is the first test comment.This is the first test comment.This is the first test comment.This is the first test comment.",
    )


  def test_comment_field_labels_and_lengths(self):

    # Check that title has the expected label
    self.assertEqual(self.comment_1._meta.get_field('blog').verbose_name, 'blog')
    self.assertEqual(self.comment_1._meta.get_field('author').verbose_name, 'author')
    self.assertEqual(self.comment_1._meta.get_field('message').verbose_name, 'message')
    self.assertEqual(self.comment_1._meta.get_field('created_at').verbose_name, 'created at')
    self.assertEqual(self.comment_1._meta.get_field('updated_at').verbose_name, 'updated at')

    self.assertTrue(self.comment_1._meta.get_field('created_at').auto_now_add)
    self.assertTrue(self.comment_1._meta.get_field('updated_at').auto_now)

    # Check that fields are not null (required fields)
    self.assertFalse(self.comment_1._meta.get_field('blog').null)
    self.assertFalse(self.comment_1._meta.get_field('author').null)
    self.assertFalse(self.comment_1._meta.get_field('message').null)
    self.assertFalse(self.comment_1._meta.get_field('created_at').null)
    self.assertFalse(self.comment_1._meta.get_field('updated_at').null)


  def test_comment_str(self):
    self.assertEqual(str(self.comment_1), self.comment_1.message[:75]+'...' if len(self.comment_1.message)>75 else self.comment_1.message[:75])
    self.assertEqual(str(self.comment_2), self.comment_2.message[:75]+'...' if len(self.comment_2.message)>75 else self.comment_2.message[:75])