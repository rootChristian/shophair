'''
************************************************************************
*************** Author:   Christian KEMGANG NGUESSOP *******************
*************** Project:   shophair                  *******************
*************** Version:  1.0.0                      *******************
************************************************************************
'''

from django.urls import path, include
from .views import GoogleOauthSignInview, RegisterUserView, VerifyUserEmail, LoginView, CheckAuthenticatedView, PasswordResetView, PasswordResetConfirm, SetNewPasswordView, LogoutView
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from rest_framework.routers import DefaultRouter

# Initialize the router
router = DefaultRouter()

# User authentication routes
auth_patterns = [
    path('register/', RegisterUserView.as_view(), name='register_user'),
    path('verify-email/', VerifyUserEmail.as_view(), name='verify_email'),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('check-profile/', CheckAuthenticatedView.as_view(), name='granted'),
    path('token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('reset-password/', PasswordResetView.as_view(), name='reset_password'),
    path('reset-password-confirm/<uidb64>/<token>/', PasswordResetConfirm.as_view(), name='reset_password_confirm'),
    path('set-new-password/', SetNewPasswordView.as_view(), name='set_new_password'),
    #path('csrf-cookie/', GetCSRFTokenView.as_view(), name='csrf_token')
    path('google/', GoogleOauthSignInview.as_view(), name='google')
]

# User management routes
user_patterns = [
    
]

# Combine all patterns
urlpatterns = [
    path('auth/', include(auth_patterns)),
    path('', include(user_patterns)),
]
