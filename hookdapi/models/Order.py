from django.db import models
from .Customer import Customer
from .Payment import Payment


class Order(models.Model):
    created_date = models.DateField(
        default="0000-00-00",
    )
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    payment = models.ForeignKey(Payment, on_delete=models.DO_NOTHING, null=True)
    total_price = models.PositiveIntegerField(default=0)
