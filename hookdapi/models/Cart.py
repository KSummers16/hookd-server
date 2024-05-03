from django.db import models
from .RTSProducts import RTSProduct
from .CusRequest import CusRequest
from .Customer import Customer


class Cart(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.CASCADE)
    created_date = models.DateTimeField(auto_now_add=True)
    quantity = models.PositiveIntegerField(default=1)

    def total_price(self):
        if self.rts_product:
            return self.rts_product.price * self.quantity
        elif self.cus_product:
            return self.cus_product.price * self.quantity
        return 0
