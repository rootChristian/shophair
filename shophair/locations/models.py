"""
***********************************************************************
************** Author:   Christian KEMGANG NGUESSOP *******************
************** Project:   shophair                  *******************
************** Version:  1.0.0                      *******************
***********************************************************************
"""

from django.db import models
from shophair.users_bk.models import User

# Model locations
class Location(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='locations')
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    city = models.CharField(max_length=20)
    state = models.CharField(max_length=20)
    postal_code = models.CharField(max_length=15)
    country = models.CharField(max_length=20)

    def __str__(self):
        return f"{self.address_line_1}, {self.city}"

    class Meta:
        verbose_name = 'Location'
        verbose_name_plural = 'Locations'
        