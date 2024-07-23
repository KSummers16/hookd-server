from django.db import models


class RTSSold(models.Model):
    name = models.CharField(max_length=50)
    price = models.IntegerField()
    sold_date = models.DateTimeField(auto_now_add=True)
    order = models.ForeignKey("Order", on_delete=models.SET_NULL, null=True)
    product_type = models.CharField(
        max_length=20,
        default="rtsproduct",
        editable=False,  # This makes the field uneditable in the admin interface
    )

    def __str__(self):
        return f"{self.name} - Sold on {self.sold_date}"
