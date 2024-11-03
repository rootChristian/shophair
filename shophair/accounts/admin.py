"""
***********************************************************************
************** Author:   Christian KEMGANG NGUESSOP *******************
************** Project:   shophair                  *******************
************** Version:  1.0.0                      *******************
***********************************************************************
"""

from django.contrib import admin
from .models import User

admin.site.register(User)
