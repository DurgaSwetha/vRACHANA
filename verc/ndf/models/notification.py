from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone
from django.utils.translation import gettext_lazy as _
from django.contrib.postgres.fields import ArrayField


class Notification():
    name = models.CharField(max_length=100)
    alt_name = models.CharField(max_length=100,blank=True)
    descrptn = models.CharField(max_length=500,blank=True)
    created_by = models.PositiveSmallIntegerField()
    scope = models.CharField(max_length=100,blank=True)
    status = models.CharField(max_length=100,blank=True)
    start_date = models.DateField()
    end_date = models.DateField()
    target_userid = models.PositiveSmallIntegerField()
    created_at = models.DateTimeField()