from django.db import models

class Ingredient(models.Model):
    name = models.TextField(unique=True)

    class Meta:
        ordering = ('name',)
        db_table = 'Ingredient'