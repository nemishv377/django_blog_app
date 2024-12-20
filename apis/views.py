from django.http import HttpResponse, JsonResponse
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework.parsers import JSONParser
from rest_framework import viewsets , status, generics
from accounts.models import Author
from blog.models import Blog
from accounts.serializers import *
from blog.serializers import *
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.exceptions import NotFound
from accounts.permissions import IsAuthorPermission
from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework_simplejwt.authentication import JWTAuthentication
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.contrib.auth.tokens import default_token_generator
from django.contrib.sites.shortcuts import get_current_site



# Create your views here.

class MyTokenObtainPairView(TokenObtainPairView):
  serializer_class = MyTokenObtainPairSerializer
  

class PasswordResetRequestView(APIView):
  permission_classes = [AllowAny]

  def post(self, request):
    email = request.data.get('email')
    
    try:
      author = Author.objects.get(email=email)
    
    except Author.DoesNotExist:
      return Response({'message': 'Password reset email has been sent.'}, status=200)

    token = default_token_generator.make_token(author)
    uid = urlsafe_base64_encode(str(author.pk).encode('utf-8'))
    reset_link = f"http://localhost:8000/accounts/reset/{uid}/{token}/"
    email_message = render_to_string('password_reset_email.html', {'reset_link': reset_link})

    send_mail(
      'Password Reset Request',
      "",
      'no-reply@example.com',
      [author.email],
      fail_silently=False,
      html_message=email_message
    )

    return Response({
        "message": "Password reset email has been sent.",
        "reset_link": f"{get_current_site(request).domain}/api/accounts/reset/{uid}/{token}/"
      }, status=200)



class PasswordResetConfirmView(APIView):
  permission_classes = [AllowAny]

  def post(self, request, uidb64, token):
  
    try:
      uid = urlsafe_base64_decode(uidb64).decode('utf-8')
      author = Author.objects.get(pk=uid)
  
    except (TypeError, ValueError, OverflowError, Author.DoesNotExist):
      return Response({'error': 'Invalid token or user ID.'}, status=400)

    if not default_token_generator.check_token(author, token):
      return Response({'error': 'Invalid token.'}, status=400)

    new_password = request.data.get('password')
    if not new_password:
      return Response({'error': 'Password is required.'}, status=400)

    author.set_password(new_password)
    author.save()

    return Response({'message': f"{author}, your password reset successful."}, status=200)
      
      
      
      

class RegisterView(generics.CreateAPIView):
  queryset = Author.objects.all()
  serializer_class = RegisterSerializer
  authentication_classes = [JWTAuthentication]
  
  def create(self, request, *args, **kwargs):
    if request.user.has_perm('author.can_add_author'):
      
      serializer = self.get_serializer(data=request.data)
      serializer.is_valid(raise_exception=True)
      self.perform_create(serializer)
      return Response({
        "message": f"{serializer.validated_data['username']} registered successfully.",
        "author": serializer.data,
      }, status=201)
    
    else:
      return Response({
        "message": "You dont have the permissison to register new blogger.",
      }, status=400)
      

  def perform_create(self, serializer):
    serializer.save()



class AuthorsViewSet(viewsets.ModelViewSet): 
  
  queryset = Author.objects.all() 
  serializer_class = AuthorSerializer
  permission_classes = [IsAuthorPermission]
  authentication_classes = [JWTAuthentication]



class BlogsViewSet(viewsets.ModelViewSet):

  queryset = Blog.objects.all().order_by('-created_at')
  serializer_class = BlogSerializer
  permission_classes = [IsAuthorPermission]
  authentication_classes = [JWTAuthentication]

  
@api_view(['POST'])
def signup(request):
  serializer = RegisterSerializer(data=request.data)
  
  if serializer.is_valid():
    serializer.save()
    return Response({
      "message": "You have successfully signed up and are now logged in!.",
      "author": serializer.data,
    }, status=201)
  
  return Response({
    "errors": serializer.errors
  }, status=400)



# @api_view(['POST'])
# @permission_classes([IsAuthenticated])
# @authentication_classes([JWTAuthentication])
# def register(request):
  
#   if request.user.has_perm('author.can_add_author'):
  
#     user_data = request.data
#     form = AuthorSignupForm(user_data)

#     if form.is_valid():
#       user = form.save()
#       author_group, created = Group.objects.get_or_create(name="Author")
#       user.groups.add(author_group)

#       serializer = AuthorSerializer(user, context={'request': request}, many=False)
#       return Response({
#         "message": f"{user.username} has successfully registered.",
#         "author": serializer.data,
#         # "group": [group.name for group in user.groups.all()]
#       }, status=201)

#     return Response({
#       "errors": form.errors
#     }, status=400)
  
#   else:
#     return Response({
#       "message": "You dont have the permissison to register new blogger.",
#     }, status=400)


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def register(request):

  if request.user.has_perm('author.can_add_author'):
    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid():
      serializer.save()
      return Response({
        "message": f"{serializer.data['username']} registered successfully.",
        "author": serializer.data
      }, status=201)

    return Response({
      "errors": serializer.errors
    }, status=400)

  else:
    return Response({
      "message": "You dont have the permissison to register new blogger.",
    }, status=400)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def profile(request):
  
  user = request.user
  serializer = AuthorSerializer(user, context={'request': request}, many=False)
  return Response({'message': 'Authenticated user', 'user': serializer.data})



@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def edit_author(request, id):

  if request.user.has_perm('author.can_change_author') or request.user.id == id:
    
    try:
      author = Author.objects.get(id=id)
  
    except Author.DoesNotExist:
      return Response({
        "message": "The blogger you are trying to edit does not exist.",
      }, status=400)

    serializer = AuthorSerializer(author, context={'request': request}, data=request.data, partial=True)

    if serializer.is_valid():
      serializer.save()
      return Response({
        "message": "Author profile updated successfully.",
        "author": serializer.data
        }, status=200)


    return Response({
        "errors": serializer.errors
    }, status=400)
    
  else:
    return Response({
      "message": "You dont have the permissison to edit the blogger.",
    }, status=400)
    


@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def delete_author(request, id):

  if request.user.has_perm('author.can_delete_author') or request.user.id == id:

    try:
      author = Author.objects.get(id=id)
  
    except Blog.DoesNotExist:
      return Response({
      "message": "The blogger you are trying to edit does not exist.",
    }, status=400)

    author.delete()
    return Response({'message': f"{author} Successfully deleted."}, status=status.HTTP_200_OK)

  else:
    return Response({
      "message": "You dont have the permissison to delete blogger.",
    }, status=400)



@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def new_blog(request):
  
  if not request.user.has_perm('author.can_add_blog'):
    return Response({
      "message": "You don't have permission to add a blog."
    }, status=403)
    
  serializer = BlogSerializer(data=request.data, context={'request': request})
  

  if serializer.is_valid():
    serializer.save()
    return Response({
      "message": "Blog created successfully.",
      "blog": serializer.data
    }, status=201)

  return Response({
    "errors": serializer.errors
  }, status=400)
  
  
  
@api_view(['PUT', 'PATCH'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def edit_blog(request, id):
  
  if not request.user.has_perm('author.can_change_blog'):
    return Response({
      "message": "You don't have permission to edit a blog."
    }, status=403)
    
  try:
    blog = Blog.objects.get(id=id)

  except Blog.DoesNotExist:
    return Response({
      "message": "The blog you are trying to edit does not exist.",
    }, status=400)
    
  serializer = BlogSerializer(blog, context={'request': request}, data=request.data, partial=True)
  
  if serializer.is_valid():
    serializer.save()
    return Response({
      "message": "Blog updated successfully.",
      "blog": serializer.data
    }, status=200)
  
  return Response({
    "errors": serializer.errors
  }, status=400)
  


@api_view(['POST'])
@permission_classes([IsAuthenticated])
@authentication_classes([JWTAuthentication])
def create_comment(request, id):
  
  try:
    blog = Blog.objects.get(id=id)

  except Blog.DoesNotExist:
    return Response({
      "message": "The comment you are trying to on a blog does not exist.",
    }, status=400)
    
  serializer = CommentSerializer(data=request.data)
  
  if serializer.is_valid():
    serializer.save(author=request.user, blog=blog)
    comment_data = {}
    comment_data['blog'] = BlogSerializer(blog, context={'request': request}).data['title']
    comment_data['author'] = AuthorSerializer(request.user, context={'request': request}).data['username']
    comment_data = {**comment_data, **serializer.data}
    return Response({
      "message": "Your comment has been posted successfully!",
      "comment": comment_data
    })

  return Response({
    "errors": serializer.errors
  }, status=400)