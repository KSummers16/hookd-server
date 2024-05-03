from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from .Eyes import Eyes
from .Category import Category


class RTSProduct(models.Model):
    name = models.CharField(max_length=50)
    price = models.FloatField(validators=[MinValueValidator(0.00)])
    description = models.CharField(max_length=255)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    pattern = models.CharField(max_length=255, null=True)
    yarn = models.CharField(max_length=255)
    eyes = models.ForeignKey(Eyes, on_delete=models.DO_NOTHING, null=True)
    image = models.ImageField(upload_to="rtsimages/", blank=True, null=True)
