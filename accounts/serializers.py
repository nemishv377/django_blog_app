from django.contrib.auth.models import Group
from accounts.models import Author
from blog.models import Blog
from rest_framework import serializers
from blog.serializers import BlogSerializer
from django.utils import timezone
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.password_validation import validate_password
from rest_framework.validators import UniqueValidator
from datetime import datetime



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


  def get_joining_date(self, obj):
    return obj.joining_date if obj.joining_date else None



class MyTokenObtainPairSerializer(TokenObtainPairSerializer):

  @classmethod
  def get_token(cls, user):
    token = super().get_token(user)
    token['username'] = user.username
    token['email'] = user.email
    return token


  def validate(self, attrs):
    data = super().validate(attrs)
    data['message'] = "Authentication successful"
    return data



class RegisterSerializer(serializers.ModelSerializer):
  password = serializers.CharField(
      write_only=True, required=True, validators=[validate_password]
  )
  password2 = serializers.CharField(write_only=True, required=True)
  joining_date = serializers.SerializerMethodField(default=timezone.now)

  # Define serializer fields for the ones you passed
  class Meta:
    model = Author
    fields = ['email', 'username', 'first_name', 'last_name', 'joining_date', 'gender', 'date_of_birth', 'state', 'city', 'password', 'password2']

  def validate(self, attrs):

    if attrs['password'] != attrs['password2']:
      raise serializers.ValidationError({"password": "Passwords do not match."})
    
    return attrs

  def create(self, validated_data):
    
    if 'joining_date' not in validated_data or not validated_data['joining_date']:
      validated_data['joining_date'] = datetime.now().date()
    
    user = Author.objects.create_user(
      username=validated_data['username'],
      email=validated_data['email'],
      password=validated_data['password'],
      first_name=validated_data.get('first_name'),
      last_name=validated_data.get('last_name'),
      joining_date=validated_data.get('joining_date'),
      gender=validated_data.get('gender'),
      date_of_birth=validated_data.get('date_of_birth'),
      state=validated_data.get('state'),
      city=validated_data.get('city')
    )
    
    author_group, created = Group.objects.get_or_create(name="Author")
    user.groups.add(author_group)


    return user
  
  def get_joining_date(self, obj):
    return obj.joining_date if obj.joining_date else None