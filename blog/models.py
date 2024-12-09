from django.db import models
from accounts.models import Author
from django.utils import timezone
from datetime import timedelta
from django.core.exceptions import ValidationError
from django.utils.translation import gettext_lazy as _

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

  @property
  def time_display(self):
    now = timezone.now()
    time_diff = now - self.created_at

    if time_diff < timedelta(hours=1):
      minutes = int(time_diff.total_seconds() // 60)
      return f'{minutes} minute{"s" if minutes != 1 else ""} ago'      
    elif time_diff < timedelta(days=1):
      hours = int(time_diff.total_seconds() // 3600)
      return f'{hours} hour{"s" if hours != 1 else ""} ago'
    else:
      days = time_diff.days
      return f'{days} day{"s" if days != 1 else ""} ago'
    
  def clean(self):
    """Validate the image file extension."""
    if self.image:
      valid_extensions = ['jpg', 'jpeg', 'png']
      file_extension = self.image.name.split('.')[-1].lower()
      if file_extension not in valid_extensions:
        raise ValidationError(_('Unsupported file extension. Use JPG, JPEG, or PNG.'))
      if self.image.size > 10 * 1024 * 1024:
        raise ValidationError(_('The image is too large. Please upload an image smaller than 10MB.'))
    super().clean()
