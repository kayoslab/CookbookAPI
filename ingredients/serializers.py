from rest_framework import serializers
from ingredients.models import Ingredient


class IngredientSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Ingredient
        fields = ('id', 'name',)