from rest_framework import serializers
from diets.models import Diet


class DietSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Diet
        fields = ('id', 'name',)