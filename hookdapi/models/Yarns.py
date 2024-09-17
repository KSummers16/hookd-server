from django.db import models
from .Companys import Company
from .Weights import Weight
from .Colors import Color
from .Customer import Customer


class MasterYarn(models.Model):
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE)
    base_color = models.ForeignKey(Color, on_delete=models.CASCADE)
    color_name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.name} - {self.color_name} ({self.base_color.name})"


class CustomerYarn(models.Model):
    master_yarn = models.ForeignKey(
        MasterYarn, null=True, blank=True, on_delete=models.SET_NULL
    )
    name = models.CharField(max_length=100)
    company = models.ForeignKey(Company, on_delete=models.CASCADE)
    weight = models.ForeignKey(Weight, on_delete=models.CASCADE)
    base_color = models.ForeignKey(Color, on_delete=models.CASCADE)
    color_name = models.CharField(max_length=100)
    amount = models.PositiveIntegerField(default=0)
    user = models.ForeignKey(Customer, on_delete=models.CASCADE)
    is_custom = models.BooleanField(default=False)

    def __str__(self):
        return f"{self.name} - {self.color_name} ({self.base_color.name})"
