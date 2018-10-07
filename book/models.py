from django.db import models
from django.conf import settings

# Create your models here.
class Blike(models.Model):
    u = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    b_id = models.CharField(max_length=50)
