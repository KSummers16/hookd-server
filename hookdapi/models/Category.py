from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Category(models.Model):

    name = models.CharField(max_length=255)
