from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .Category import Category
from .Eyes import Eyes


class CusProduct(models.Model):
    name = models.CharField(max_length=100)
    price = models.IntegerField()
    image = models.CharField(max_length=255, null=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pattern = models.CharField(max_length=100)
    yarn = models.CharField(max_length=100)
    eyes = models.ForeignKey(Eyes, on_delete=models.DO_NOTHING, null=True)
