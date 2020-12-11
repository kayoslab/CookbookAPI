from django.db import models

class Diet(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        ordering = ('name',)
        db_table = 'Diet'