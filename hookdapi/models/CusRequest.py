from django.db import models
from .CusProducts import CusProduct
from .Eyes import Eyes
from .Customer import Customer
from .Colors import Color


class CusRequest(models.Model):
    cus_product = models.ForeignKey(CusProduct, on_delete=models.CASCADE)
    eyes = models.ForeignKey(Eyes, on_delete=models.CASCADE, null=True)
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    color1 = models.ForeignKey(
        Color, on_delete=models.CASCADE, related_name="color1_requests"
    )
    color2 = models.ForeignKey(
        Color, on_delete=models.CASCADE, null=True, related_name="color2_requests"
    )
