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
import random
import datetime
from accounts.security import create_token, decrypt_token
from rest_framework_simplejwt.tokens import RefreshToken
from drf_yasg.utils import swagger_auto_schema 

# Create your views here.

class BloggerViewSet(viewsets.ModelViewSet):
  queryset = Author.objects.all().order_by('-date_joined')
  serializer_class = AuthorSerializer
  permission_classes = [permissions.IsAuthenticated]
  authentication_classes = [JWTAuthentication]


  def create(self,request):

    if not request.user.has_perm('can_add_author'):
      return Response(
        {"detail": "You are not authorized to add an blogger."},
        status=403
      )

    serializer = RegisterSerializer(data=request.data)

    if serializer.is_valid(raise_exception=True):
      user = serializer.save()
      refresh_token = RefreshToken.for_user(user)
      access_token = refresh_token.access_token

      return Response({
        "refresh": str(refresh_token),
        "access": str(access_token),
        "message": "Blogger registered successfully.",
        "author": serializer.data,
      }, status=201)

    return Response({
      "errors": serializer.errors
    }, status=400)


  def update(self, request, pk=None):
    
    if not request.user.has_perm('can_change_author'):
      return Response({
        "detail": "You are not authorized to update an blogger."},
        status=403
      )

    instance = self.get_object()
    serializer = self.get_serializer(instance, data=request.data, partial=True)
    serializer.is_valid(raise_exception=True)
    serializer.save()
    response_data = serializer.data
    response_data['message'] = 'Blogger updated successfully.'
    return Response(response_data, status=200)


  def destroy(self, request, pk=None):

    if not request.user.has_perm('can_delete_author'):
      return Response({
        "detail": "You are not authorized to delete an blogger."
      }, status=403)

    instance = self.get_object()
    instance.delete()
    return Response({
      "detail": "Blogger deleted successfully."
    }, status=200)



class BlogViewSet(viewsets.ModelViewSet):
  queryset = Blog.objects.all().order_by('-created_at')
  serializer_class = BlogSerializer
  permission_classes = [permissions.IsAuthenticated]
  authentication_classes = [JWTAuthentication]



@swagger_auto_schema(
  method='post',
  request_body=RegisterSerializer,
  responses={201: RegisterSerializer, 400: 'Bad Request'}
)
@api_view(['POST'])
def signup(request):

  if request.user.is_authenticated:
    return Response({
      "message": "You are already logged in, you cannot sign up again."
    }, status=400)

  serializer = RegisterSerializer(data=request.data)

  if serializer.is_valid(raise_exception=True):
    user = serializer.save()
    refresh_token = RefreshToken.for_user(user)
    access_token = refresh_token.access_token

    return Response({
      "refresh": str(refresh_token),
      "access": str(access_token),
      "message": "You have successfully signed up and are now logged in!!.",
      "author": serializer.data,
    }, status=201)

  return Response({
    "errors": serializer.errors
  }, status=400)



class PasswordResetRequestView(GenericAPIView):
  serializer_class = PasswordResetRequestSerializer

  def post(self, request):
    email = request.data.get('email')

    if not email:
      return Response({"error": "Email is required."}, status=400)

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
      email_message,
      'no-reply@example.com',
      [author.email],
      fail_silently=False,
    )

    return Response({
      "message": "Password reset email has been sent.",
      "reset_link": f"{get_current_site(request).domain}/api/accounts/reset/{uid}/{token}/"
    }, status=200)



class PasswordResetConfirmView(GenericAPIView):
  serializer_class = PasswordResetConfirmSerializer

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
    return Response({'message': f"{author}, your password reset successfully."}, status=200)



class ForgetPasswordView(GenericAPIView):
  serializer_class = ForgotPasswordSerializer

  def post(self, request, *args, **kwargs):
    serilaizer = self.serializer_class(data=request.data)
    serilaizer.is_valid(raise_exception=True)
    email = serilaizer.validated_data['email']

    try:
      author = Author.objects.get(email=email)

    except Author.DoesNotExist:
      return Response({
        'detail':"Author with the given email not found."
      }, status=200)

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
          'message': 'OTP matched, access granted.'
        }, status=200)

      else:
        return Response({
          'message': 'OTP expired or invalid....'
        }, status=400)

    else:
      return Response({
        'message': 'Token invalid. Try Again!!',
      }, status=400)