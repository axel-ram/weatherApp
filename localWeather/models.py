from django.db import models
from django.contrib.auth.models import User
class Device(models.Model):
    device = models.CharField(max_length=50)
    def __str__(self):
        return self.device
class City(models.Model):
    class Meta:
        verbose_name_plural='cities'

    name = models.CharField(max_length=20)
    device = models.ForeignKey(Device, blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.device.device[:10]+"/"+self.name