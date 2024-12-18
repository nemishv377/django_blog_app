from accounts.models import Author
from blog.models import Blog
from rest_framework import serializers
from django.core.exceptions import ValidationError


class BlogSerializer(serializers.ModelSerializer):
  
  class Meta:
    model = Blog
    fields = ['url', 'id', 'title', 'content', 'image', 'author', 'created_at', 'updated_at']


  def validate_image(self, value):

    if value:
      valid_extensions = ['jpeg', 'jpg', 'png']

      if not value.name.split('.')[-1].lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Use JPG, JPEG, or PNG.")

    return value