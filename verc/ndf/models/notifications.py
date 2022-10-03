from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
import datetime

#from .managers import UserCustomManager


class Notification(models.Model):
    name = models.CharField(max_length=100)
    alt_name = models.CharField(max_length=100)
    description = models.CharField(max_length=100)
    scope = models.CharField(max_length=100,blank=True)
    status = models.CharField(max_length=100,blank=True)
    start_date = models.DateTimeField(separator=':',Required = True, default = datetime.datetime.utcnow)
    end_date = models.DateTimeField(separator=':',Required = True, default = datetime.datetime.utcnow)
    target_userid = models.ForeignKey("TargetUser",on_delete=models.SET_NULL, null=True)
    created_at = models.DateTimeField(separator=':',Required = True, default = datetime.datetime.utcnow)
    
    