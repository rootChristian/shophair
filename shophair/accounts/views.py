"""
***********************************************************************
************** Author:   Christian KEMGANG NGUESSOP *******************
************** Project:   shophair                  *******************
************** Version:  1.0.0                      *******************
***********************************************************************
"""

from django.shortcuts import render
from .models import OneTimePassword, User
from .utils import sendOtpCodeToEmail
from .serializers import GoogleSignInSerializer, UserRegisterSerializer, LoginSerializer, PasswordResetSerializer, SetNewPasswordSerializer, LogoutSerializer 
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics, status
from django.utils.http import urlsafe_base64_decode
from django.utils.encoding import smart_str, DjangoUnicodeDecodeError
from rest_framework.response import Response

class RegisterUserView(generics.GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        #print("Request data: ", request.data)  # Debugging line

        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            sendOtpCodeToEmail(user_data['email'])

            return Response({ 
                "data": user_data,
                "message": "Thanks for signing up, a passcode has been sent to verify your email",
            }, status=status.HTTP_201_CREATED)
        
class VerifyUserEmail(generics.GenericAPIView):

    def post(self, request):
        try:
            passcode = request.data.get("otp")
            user_pass_obj=OneTimePassword.objects.get(otp=passcode)
            user=user_pass_obj.user

            if not user.is_verified:
                user.is_verified=True
                user.save()
                return Response({
                    "message": "Account email verified successfully"
                }, status=status.HTTP_200_OK)
            
            return Response({
                "message": "Passcode is invalid, user is already verified"
            }, status=status.HTTP_204_NO_CONTENT)
        
        except OneTimePassword.DoesNotExist as identifier:
            return Response({
                "message": "Passcode not provided"
            }, status=status.HTTP_400_BAD_REQUEST)
        

class LoginView(generics.GenericAPIView):
    serializer_class=LoginSerializer

    def post(self, request):
        serializer= self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response({ 
                "data": serializer.data,
                "message": "User authenticated",
        }, status=status.HTTP_200_OK)

class CheckAuthenticatedView(generics.GenericAPIView):
    permission_classes=[IsAuthenticated]

    def get(self, request):
        data={
            "message":"Its works"
        }
        return Response(data, status=status.HTTP_200_OK)

class PasswordResetView(generics.GenericAPIView):
    serializer_class=PasswordResetSerializer

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response({
            "message": "We have sent you a link to reset your password"
        }, status=status.HTTP_200_OK)
        # return Response({'message':'user with that email does not exist'}, status=status.HTTP_400_BAD_REQUEST)
    
class PasswordResetConfirm(generics.GenericAPIView):

    def get(self, request, uidb64, token):
        try:
            user_id=smart_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                return Response({
                    "message": "Token is invalid or has expired"
                }, status=status.HTTP_401_UNAUTHORIZED)
            return Response({
                "success": True, 
                "message": "Credentials is valid", 
                'uidb64':uidb64, 
                "token": token
            }, status=status.HTTP_200_OK)

        except DjangoUnicodeDecodeError as identifier:
            return Response({
                "message": "Token is invalid or has expired"
            }, status=status.HTTP_401_UNAUTHORIZED)
  
class SetNewPasswordView(generics.GenericAPIView):
    serializer_class=SetNewPasswordSerializer

    def patch(self, request):
        serializer=self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        return Response({
            "success": True, 
            "message": "Password reset is successful"
        }, status=status.HTTP_200_OK)

class LogoutView(generics.GenericAPIView):
    serializer_class=LogoutSerializer
    permission_classes = [IsAuthenticated]

    def post(self, request):
        serializer=self.serializer_class(data=request.data, context={"request": request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(status=status.HTTP_204_NO_CONTENT)
 
class GoogleOauthSignInview(generics.GenericAPIView):
    serializer_class=GoogleSignInSerializer

    def post(self, request):
        print(request.data)
        serializer=self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)
        data=((serializer.validated_data)['access_token'])
        return Response(data, status=status.HTTP_200_OK) 