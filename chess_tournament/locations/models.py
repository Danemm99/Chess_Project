from django.db import models


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255)
    city = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
