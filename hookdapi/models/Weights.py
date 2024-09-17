from django.db import models


class Weight(models.Model):
    name = models.CharField(max_length=100)
