from django.db import models

class Holiday(models.Model):
    name = models.CharField(max_length=100)
    date = models.DateField()
    is_active = models.BooleanField(default=True)
    subject_to_change = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
    class Meta:
        ordering = ['date']

# Create your models here.
