from django.contrib.auth.models import Group
from accounts.models import Author
from blog.models import Blog
from rest_framework import serializers
from blog.serializers import BlogSerializer
from django.utils import timezone
from django.contrib.auth.password_validation import validate_password
from datetime import datetime



class GroupSerializer(serializers.ModelSerializer):
  class Meta:
    model = Group
    fields = ['name']  



class AuthorSerializer(serializers.ModelSerializer):
  blogs = BlogSerializer(many=True, read_only=True)
  groups = GroupSerializer(many=True, read_only=True)


  class Meta:
    model = Author
    fields = ['url', 'id', 'email', 'username', 'first_name', 'last_name', 'joining_date', 'gender', 'date_of_birth', 'groups',  'state', 'city', 'blogs']
    extra_kwargs = {
      'url': {'view_name': 'blogger-detail'}
    }


class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  joining_date = serializers.SerializerMethodField(default=timezone.now)

  
  class Meta:
    model = Author
    fields = ['email', 'username', 'first_name', 'last_name', 'joining_date', 'gender', 'date_of_birth', 'state', 'city', 'password']


  def create(self, validated_data):
    password = validated_data.pop('password')

    if 'joining_date' not in validated_data or not validated_data['joining_date']:
      validated_data['joining_date'] = datetime.now().date()

    user = self.Meta.model(**validated_data)
    user.set_password(password)
    user.save()
    author_group, created = Group.objects.get_or_create(name="Author")
    user.groups.add(author_group)
    return user


  def get_joining_date(self, obj):
    return obj.joining_date if obj.joining_date else None



class PasswordResetRequestSerializer(serializers.Serializer):
  email = serializers.CharField(max_length=100)



class PasswordResetConfirmSerializer(serializers.Serializer):
  new_password = serializers.CharField(write_only=True, required=True, validators=[validate_password])
  new_password_confirmation = serializers.CharField(write_only=True, required=True)



class ForgotPasswordSerializer(serializers.Serializer):
  email = serializers.CharField(max_length=100)



class CheckOTPSerializer(serializers.Serializer):
  otp = serializers.CharField(max_length=6)
  token = serializers.CharField()