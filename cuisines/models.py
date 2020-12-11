from django.db import models

class Cuisine(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        ordering = ('name',)
        db_table = 'Cuisine'