from django.shortcuts import render
from rest_framework.response import Response
from accounts.models import Author
from rest_framework import permissions, viewsets
from accounts.serializers import *
from blog.serializers import *
from rest_framework.decorators import api_view, action

# Create your views here.

class BloggerViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all().order_by('-date_joined')
  serializer_class = AuthorSerializer
  permission_classes = [permissions.IsAuthenticated]



class BlogViewSet(viewsets.ModelViewSet):
  queryset = Blog.objects.all().order_by('-created_at')
  serializer_class = BlogSerializer
  permission_classes = [permissions.IsAuthenticated]
  

@api_view(['GET', 'POST'])
def signup(request):
  
  if request.user.is_authenticated:
    return Response({
      "message": "You are already logged in, you cannot sign up again."
    }, status=400)
  
  if request.method == 'POST':
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({
        "message": "You have successfully signed up!.",
        "author": serializer.data,
      }, status=201)

    return Response({
      "errors": serializer.errors
    }, status=400)
  
  return Response({
    "message": "Signup is a POST-only action."
  }, status=405)