from django.db import models
from django.urls import reverse

class Bear(models.Model):
    name = models.CharField(max_length=50)
    species = models.CharField(max_length=50)
    description = models.TextField(max_length=250)
    age = models.IntegerField()

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('bears_detail', kwargs={'bear_id': self.id})
