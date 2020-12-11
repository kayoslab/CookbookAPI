import os
from django.db import models
from cuisines.models import Cuisine
from diets.models import Diet
from ingredients.models import Ingredient
from occasions.models import Occasion


class Recipe(models.Model):
    name = models.TextField(unique=True)
    created = models.DateTimeField(auto_now_add=True)
    url = models.URLField(blank=True, null=True, default="")
    note = models.TextField(blank=True, null=True, default="")
    file = models.FileField(blank=True, null=True)

    cuisines = models.ManyToManyField(Cuisine, blank=True, default=[])
    diets = models.ManyToManyField(Diet, blank=True, default=[])
    ingredients = models.ManyToManyField(Ingredient, blank=True, default=[])
    occasions = models.ManyToManyField(Occasion, blank=True, default=[])

    @property
    def file_url(self):
        return self.get_file_url

    @property
    def get_file_url(self):
        if self.file and hasattr(self.file, 'url'):
            return self.file.url
        else:
            return None

    @property
    def file_name(self):
        return os.path.basename(self.file.name)

    class Meta:
        ordering = ('name',)
        db_table = 'Recipe'
