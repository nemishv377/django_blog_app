from django.shortcuts import render
from rest_framework.response import Response
from accounts.models import Author
from rest_framework import permissions, viewsets
from accounts.serializers import *
from rest_framework.decorators import action

# Create your views here.

class BloggerViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all().order_by('-date_joined')
  serializer_class = AuthorSerializer
  permission_classes = [permissions.IsAuthenticated]
