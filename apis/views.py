from django.shortcuts import render
from rest_framework.response import Response
from accounts.models import Author
from rest_framework import permissions, viewsets
from accounts.serializers import *
from blog.serializers import *
from rest_framework.decorators import api_view, permission_classes, authentication_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.tokens import default_token_generator
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string
from django.core.mail import send_mail
from django.contrib.sites.shortcuts import get_current_site
from rest_framework.generics import GenericAPIView
from django.shortcuts import get_object_or_404
import random
import datetime
from accounts.security import create_token, decrypt_token
from rest_framework_simplejwt.tokens import RefreshToken

# Create your views here.

class BloggerViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all().order_by('-date_joined')
  serializer_class = AuthorSerializer
  permission_classes = [permissions.IsAuthenticated]
  authentication_classes = [JWTAuthentication]



class BlogViewSet(viewsets.ModelViewSet):
  queryset = Blog.objects.all().order_by('-created_at')
  serializer_class = BlogSerializer
  permission_classes = [permissions.IsAuthenticated]
  authentication_classes = [JWTAuthentication]
  


@api_view(['POST'])
def signup(request):
  
  if request.user.is_authenticated:
    return Response({
      "message": "You are already logged in, you cannot sign up again."
    }, status=400)
  
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



class PasswordResetRequestView(APIView):

  def post(self, request):
    email = request.data.get('email')

    try:
      author = Author.objects.get(email=email)

    except Author.DoesNotExist:
      return Response({'message': 'Password reset email has been sent.'}, status=200)

    token = default_token_generator.make_token(author)
    uid = urlsafe_base64_encode(str(author.pk).encode('utf-8'))
    reset_link = f"{get_current_site(request).domain}/api/accounts/reset/{uid}/{token}/"
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
  
  def post(self, request, uidb64, token):

    try:
      uid = urlsafe_base64_decode(uidb64).decode('utf-8')
      author = Author.objects.get(pk=uid)

    except (TypeError, ValueError, OverflowError, Author.DoesNotExist):
      return Response({'error': 'Invalid token or user ID.'}, status=400)

    if not default_token_generator.check_token(author, token):
      return Response({'error': 'Invalid token.'}, status=400)

    new_password = request.data.get('new_password')
    new_password_confirmation = request.data.get('new_password_confirmation')

    if not new_password or not new_password_confirmation:
      return Response({'error': 'Both password and password confirmation are required.'}, status=400)
    
    if new_password != new_password_confirmation:
      return Response({'error': 'The two password fields didn’t match.'}, status=400)

    author.set_password(new_password)
    author.save()
    return Response({'message': f"{author}, your password reset successful."}, status=200)
  
  

class ForgetPasswordView(GenericAPIView):
  serializer_class = ForgotPasswordSerializer

  def post(self, request, *args, **kwargs):
    serilaizer = self.serializer_class(data=request.data)
    serilaizer.is_valid(raise_exception=True)
    email = serilaizer.validated_data['email']
    author = get_object_or_404(Author, email=email)
    otp = str(random.randint(100000, 999999))
    payload = {
      'user_id': author.id,
      'email': author.email,
      'otp': otp,
      'exp': datetime.datetime.now() + datetime.timedelta(minutes=5)
    }
    token = create_token(payload)

    send_mail(
      'OTP for Forget Password',
      f'Your Otp is {otp}',
      'no-reply@example.com',
      [author.email],
    )
    
    return Response({
      'token': token
    }, status=200)



class CheckOTPView(GenericAPIView):
  serializer_class = CheckOTPSerializer

  def post(self, request, *args, **kwargs):

    serialzier = self.serializer_class(data=request.data)
    serialzier.is_valid(raise_exception=True)
    otp = serialzier.validated_data['otp']
    enc_token = serialzier.validated_data['token']
    data = decrypt_token(enc_token)

    if data['status']:
      otp_real = data['payload']['otp']

      if otp == otp_real:
        email = data['payload']['email']
        author = Author.objects.get(email=email)
        access_token = str(RefreshToken.for_user(author).access_token)

        return Response({
          'access_token': access_token,
          'status': True,
        }, status=200)

      else:
        return Response({
          'message': 'OTP didnt matched....'
        }, status=400)

    else:
      return Response({
        'message': 'OTP expired...Try Again!!',
        'status': False
      }, status=400)