from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['date']

# Create your models here.
