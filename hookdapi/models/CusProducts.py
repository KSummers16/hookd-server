from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .Category import Category


class CusProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image_path = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pattern = models.CharField(max_length=100)
    yarn = models.CharField(max_length=100)
