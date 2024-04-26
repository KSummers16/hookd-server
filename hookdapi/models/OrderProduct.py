from django.db import models
from .Order import Order
from .RTSproducts import RTSProduct
from .CusRequest import CusRequest


class OrderProduct(models.Model):
    order = models.ForeignKey(Order, on_delete=models.CASCADE)
    rtsproduct = models.ForeignKey(RTSProduct, null=True, on_delete=models.CASCADE)
    cusrequest = models.ForeignKey(CusRequest, null=True, on_delete=models.CASCADE)
