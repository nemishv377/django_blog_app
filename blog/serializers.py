from accounts.models import Author
from blog.models import Blog, Comment
from rest_framework import serializers
from django.core.exceptions import ValidationError
from rest_framework.relations import HyperlinkedIdentityField


class CommentSerializer(serializers.ModelSerializer):

  class Meta:
    model = Comment
    fields = ['message']


class BlogSerializer(serializers.ModelSerializer):
  
  comments = CommentSerializer(many=True, read_only=True)
  url = serializers.HyperlinkedIdentityField(view_name='blog-detail', lookup_field='pk')
  
  class Meta:
    model = Blog
    fields = ['url', 'id', 'title', 'content', 'image', 'author', 'created_at', 'updated_at', 'comments']

  image = serializers.ImageField(required=False, allow_null=True)


  def validate_image(self, value):

    if value:
      valid_extensions = ['jpeg', 'jpg', 'png']

      if not value.name.split('.')[-1].lower() in valid_extensions:
        raise ValidationError("Unsupported file extension. Use JPG, JPEG, or PNG.")

    return value