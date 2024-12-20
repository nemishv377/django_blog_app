from django.test import TestCase
from django.urls import reverse
from blog.tests.test_models import BlogModelTestBase
import math


class BlogViewTest(BlogModelTestBase):
  
  def test_blog_detail(self):
    url = reverse('blog_detail', kwargs={'id': self.blog.id})
    response = self.client.get(url)

    self.assertContains(response, self.blog.title)
    self.assertContains(response, self.blog.content)  
    self.assertContains(response, self.blog.author.get_full_name())


  def test_blog_list_view(self):
    response = self.client.get('/blog/blogs/')
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/blogs_list.html')


  def test_blog_list_view_at_named_url(self):
    response = self.client.get(reverse('blogs'))
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/blogs_list.html')


  def test_blog_list_pagination(self):

    url = reverse('blogs')
    response = self.client.get(url)
    self.assertEqual(response.status_code, 200)
    self.assertTemplateUsed(response, 'blog/blogs_list.html')

    total_items = self.Blog.objects.count()
    total_pages = math.ceil(total_items / 5)

    for page_num in range(1, total_pages + 1):
      response_page = self.client.get(url + f'?page={page_num}')

      if page_num == total_pages:
        expected_items = total_items % 5 or 5

      else:
        expected_items = 5  

      self.assertEqual(len(response_page.context['page_obj']), expected_items)