from django.db import models

class Advertise(models.Model):
    adimage = models.ImageField(blank = True, upload_to="advertise/%Y%m%d")
    adname = models.CharField(max_length=50, blank = True)
    brandDetail = models.TextField(blank=True)
    adurl = models.TextField(blank=True)
