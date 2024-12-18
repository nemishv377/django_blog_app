from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.parsers import JSONParser
from rest_framework import viewsets , status
from accounts.models import Author
from blog.models import Blog
from accounts.serializers import AuthorSerializer
from blog.serializers import BlogSerializer
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from accounts.permissions import IsAuthorPermission


# Create your views here.
class AuthorsViewSet(viewsets.ModelViewSet): 
  
  queryset = Author.objects.all() 
  serializer_class = AuthorSerializer
  permission_classes = [IsAuthorPermission]
  
  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(
        {"message": "Author successfully created", "author": serializer.data},
        status=status.HTTP_201_CREATED,
      )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


  def update(self, request, *args, **kwargs):

    partial = kwargs.pop('partial', False)
    instance = self.get_object()

    serializer = self.get_serializer(instance, data=request.data, partial=partial)
    
    if serializer.is_valid():
      serializer.save()
      return Response(
        {
          "message": f"{instance} successfully updated",
          "author": serializer.data
        },
        status=status.HTTP_200_OK,
      )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  

  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    instance.delete()
    return Response({"detail": f"{instance} Successfully deleted."}, status=status.HTTP_204_NO_CONTENT)



class BlogsViewSet(viewsets.ModelViewSet):

  queryset = Blog.objects.all().order_by('-created_at')
  serializer_class = BlogSerializer
  permission_classes = [IsAuthorPermission]


  def create(self, request, *args, **kwargs):
    serializer = self.get_serializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response(
        {"message": "Blog successfully created", "blog": serializer.data},
        status=status.HTTP_201_CREATED,
      )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
  def update(self, request, *args, **kwargs):
    instance = self.get_object()
    data = request.data.copy()

    if 'image' not in data or not request.FILES.get('image'):
      data['image'] = instance.image

    serializer = self.get_serializer(instance, data=data, partial=kwargs.get('partial', False))

    if serializer.is_valid():
      serializer.save()
      return Response(
        {"message": f"{instance} successfully updated", "blog": serializer.data},
        status=status.HTTP_200_OK,
      )

    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
  
  
  def destroy(self, request, *args, **kwargs):
    instance = self.get_object()
    instance.delete()
    return Response({"detail": f"{instance} successfully deleted."}, status=status.HTTP_204_NO_CONTENT)