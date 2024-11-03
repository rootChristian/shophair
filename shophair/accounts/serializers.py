"""
***********************************************************************
************** Author:   Christian KEMGANG NGUESSOP *******************
************** Project:   shophair                  *******************
************** Version:  1.0.0                      *******************
***********************************************************************
"""

from rest_framework import serializers
from django.contrib.auth import authenticate
from rest_framework.exceptions import AuthenticationFailed
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from .providers import Google, registerSocialUser
from ..shophair.settings import base
from .utils import sendNormalEmail
from string import ascii_lowercase, ascii_uppercase
from django.utils.encoding import smart_str, force_str, force_bytes
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from .models import User


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    confirm_password = serializers.CharField(max_length=50, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ["email", "first_name", "last_name", "password", "confirm_password"]

    def validate(self, attrs):
        password = attrs.get("password", "")
        confirm_password = attrs.get("confirm_password", "")

        if password != confirm_password:
            raise serializers.ValidationError("Passwords do not match")
        return attrs
    
    def create(self, validated_data):
        user = User.objects.create_user(
            email=validated_data["email"],
            first_name=validated_data.get("first_name"),
            last_name=validated_data.get("last_name"),
            password=validated_data.get("password")
        )
        return user

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=50, min_length=6)
    full_name=serializers.CharField(max_length=100, read_only=True)
    password=serializers.CharField(max_length=50, write_only=True)
    access_token=serializers.CharField(max_length=255, read_only=True)
    refresh_token=serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ["email", "full_name", "password", "access_token", "refresh_token"]

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        request=self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Invalid credential try again")
        if not user.is_verified:
            raise AuthenticationFailed("Email is not verified")
        
        # Generate token
        tokens=user.tokens()

        return {
            'email':user.email,
            'full_name':user.get_full_name,
            "access_token":str(tokens.get('access')),
            "refresh_token":str(tokens.get('refresh'))
        }
    
class PasswordResetSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=50)

    class Meta:
        fields = ['email']
    
    def validate(self, attrs):
        email = attrs.get('email')

        try:
            #print("\nTESTING", email, "\n")
            user = User.objects.get(email=email)
            uidb64 = urlsafe_base64_encode(force_bytes(user.id))
            token = PasswordResetTokenGenerator().make_token(user)
            request = self.context.get('request')
            current_site = get_current_site(request).domain
            relative_link = reverse('reset_password_confirm', kwargs={'uidb64': uidb64, 'token': token})
            abslink = f"http://{current_site}{relative_link}"
            email_body = (
                f"Hi {user.first_name},\n"
                f"Please use the link below to reset your password {abslink}\n\n"
                f"Best regards,\n"
                f"Shophair Company"
            )
            data = {
                "email_body": email_body,
                "email_subject": "Reset your Password",
                "to_email": user.email
            }
            sendNormalEmail(data)
            
        except User.DoesNotExist:
            #print(f"User with email {email} does not exist")
            raise serializers.ValidationError("A user with this email does not exist.")
        
        except Exception as e:
            #print(f"An error occurred: {str(e)}")
            raise serializers.ValidationError("An unexpected error occurred. Please try again later.")

        return attrs #super().validate(attrs)

class SetNewPasswordSerializer(serializers.Serializer):
    old_password = serializers.CharField(max_length=50, min_length=8, write_only=True)
    password=serializers.CharField(max_length=50, min_length=8, write_only=True)
    confirm_password=serializers.CharField(max_length=50, min_length=8, write_only=True)
    uidb64=serializers.CharField(min_length=1, write_only=True)
    token=serializers.CharField(min_length=3, write_only=True)

    class Meta:
        fields = ["old_password", "password", "confirm_password", "uidb64", "token"]

    def validate(self, attrs):
        token=attrs.get("token")
        uidb64=attrs.get("uidb64")
        old_password = attrs.get("old_password")
        password=attrs.get("password")
        confirm_password=attrs.get("confirm_password")
        
        if password != confirm_password:
            raise serializers.ValidationError({"confirm_password": "Passwords do not match."})
        
        try:
            user_id=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(id=user_id)

            if not PasswordResetTokenGenerator().check_token(user, token):
                raise serializers.ValidationError({"token": "Reset link is invalid or has expired."})
            
            if not user.check_password(old_password):
                raise serializers.ValidationError({"old_password": "Current password is incorrect."})

            if password == old_password:
                raise serializers.ValidationError({"password": "New password must be different from the old password."})

            user.set_password(password)
            user.save()
        
        except User.DoesNotExist:
            raise serializers.ValidationError({"uidb64": "Invalid token or user does not exist."})
        
        except (ValueError, TypeError):
            raise serializers.ValidationError({"uidb64": "Invalid token or user ID."})
        
        except Exception as e:
            #print(f"An error occurred: {str(e)}")
            raise serializers.ValidationError({"error": "An unexpected error occurred. Please try again."})

        return attrs

class LogoutSerializer(serializers.Serializer):
    refresh_token=serializers.CharField()

    default_error_message = {
        "bad_token": ("Token is expired or invalid")
    }

    def validate(self, attrs):
        self.token = attrs.get("refresh_token")
        return attrs

    def save(self, **kwargs):
        try:
            token=RefreshToken(self.token)
            token.blacklist()
        except TokenError:
            return self.fail("bad_token")
        
class GoogleSignInSerializer(serializers.Serializer):
    access_token=serializers.CharField(min_length=6)

    def validateAccessToken(self, access_token):
        user_data=Google.validate(access_token)
        try:
            user_data['sub']
            
        except:
            raise serializers.ValidationError("this token has expired or invalid please try again")
        
        if user_data['aud'] != base.GOOGLE_CLIENT_ID:
                raise AuthenticationFailed('Could not verify user.')

        user_id=user_data['sub']
        email=user_data['email']
        first_name=user_data['given_name']
        last_name=user_data['family_name']
        provider='google'

        return registerSocialUser(provider, email, first_name, last_name)
