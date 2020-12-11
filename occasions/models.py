from django.db import models

class Occasion(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        ordering = ('name',)
        db_table = 'Occasion'