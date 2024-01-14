from django.db import models


class Location(models.Model):
    location_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=255, null=True, blank=True)
    city = models.CharField(max_length=255, null=True, blank=True)
    address = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        unique_together = ['name', 'city', 'address']

    def __str__(self):
        if self.name is None:
            return 'Online'
        else:
            return f'{self.name}, {self.city}, {self.address}'
