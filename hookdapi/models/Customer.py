from django.db import models
from django.contrib.auth.models import User


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    address = models.CharField(max_length=255)
    email_address = models.EmailField()
    name = models.CharField(max_length=100)

    def is_admin(self):
        return self.user.is_superuser
