'''
************************************************************************
*************** Author:   Christian KEMGANG NGUESSOP *******************
*************** Project:   shophair                  *******************
*************** Version:  1.0.0                      *******************
************************************************************************
'''

from django.contrib import admin
from django.urls import path, include
from dotenv import load_dotenv
import os
#from django.views.generic import TemplateView
#from users_bk import views  # Import your views

# Load environment variables from .env file
load_dotenv()

# Access to API versions
api_version = os.getenv("API_VERSION", "v1")  # Default to v1 if not set

urlpatterns = [
    path("admin/", admin.site.urls),
    path(f"{api_version}/", include('accounts.urls')),
    #path(f"{api_version}/users/", include('users.urls')),  # Include users' URLs
]

#urlpatterns += [re_path(r'^.*', TemplateView.as_view(template_name='index.html'))]
