from django.db import models
from accounts.models import Author

# Create your models here.
class Blog(models.Model):
  title = models.CharField(max_length=200, null=False, unique=True)
  content = models.TextField(null=False)
  created_at = models.DateTimeField(auto_now_add=True, null=False)
  updated_at = models.DateTimeField(auto_now=True, null=False)
  image = models.ImageField(upload_to='blog_images/', null=False)
  author = models.ForeignKey(Author, on_delete=models.CASCADE, related_name='blogs', null=False)
  
  class Meta:
    db_table = 'blog'
  
  def __str__(self):
    return self.title

