from rest_framework import serializers
from cuisines.models import Cuisine


class CuisineSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Cuisine
        fields = ('id', 'name',)