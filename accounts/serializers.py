from django.contrib.auth.models import Group
from accounts.models import Author
from blog.models import Blog
from rest_framework import serializers
from blog.serializers import BlogSerializer
from django.utils import timezone


class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = Group
    fields = ['name']  



class AuthorSerializer(serializers.ModelSerializer):
  blogs = BlogSerializer(many=True, read_only=True)
  groups = GroupSerializer(many=True, read_only=True)
  joining_date = serializers.SerializerMethodField(default=timezone.now)

  class Meta:
    model = Author
    fields = ['url', 'id', 'email', 'username', 'first_name', 'last_name', 'joining_date', 'gender', 'date_of_birth', 'groups',  'state', 'city', 'blogs']
    extra_kwargs = {
      'url': {'view_name': 'blogger-detail'}
    }


  def get_joining_date(self, obj):
    return obj.joining_date if obj.joining_date else None