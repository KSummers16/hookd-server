from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.DO_NOTHING)
    address = models.CharField(max_length=255)
    email_address = models.EmailField()
    name = models.CharField(max_length=100)
    is_admin = models.BooleanField(default=False)
