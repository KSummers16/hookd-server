from django.db import models


class Eyes(models.Model):

    name = models.CharField(max_length=75)
