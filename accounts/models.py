from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.utils.translation import gettext_lazy as _
from django.utils import timezone

class AuthorManager(BaseUserManager):
  def create_user(self, email, username, password=None, **extra_fields):
    if not email:
      raise ValueError(_('The Email field must be set'))
    email = self.normalize_email(email)
    user = self.model(email=email, username=username, **extra_fields)
    user.set_password(password)
    user.save(using=self._db)
    return user
  
  def create_superuser(self, email, username, password=None, **extra_fields):
    extra_fields.setdefault('is_staff', True)
    extra_fields.setdefault('is_superuser', True)
    return self.create_user(email, username, password, **extra_fields)

class Author(AbstractUser):
  GENDER_CHOICES = [('Male', 'Male'), ('Female', 'Female'), ('Other', 'Other')]
  
  email = models.EmailField(unique=True, null=False)  
  first_name = models.CharField(max_length=30, null=False)  
  last_name = models.CharField(max_length=30, null=False)  
  joining_date = models.DateField(default=timezone.now)  
  gender = models.CharField(max_length=20, choices=GENDER_CHOICES, null=False)  
  date_of_birth = models.DateField(null=False)  
  state = models.CharField(max_length=30, null=False)  
  city = models.CharField(max_length=30, null=False) 
  
  USERNAME_FIELD = 'email'
  REQUIRED_FIELDS = ['username', 'first_name', 'last_name', 'gender', 'date_of_birth', 'state', 'city']
  
  objects = AuthorManager()
  
  class Meta:
    db_table = 'author'

  def __str__(self):
    return self.username