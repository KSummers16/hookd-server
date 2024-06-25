from django.db import models


class RTSSold(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    sold_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f"{self.name} - Sold on {self.sold_date}"
