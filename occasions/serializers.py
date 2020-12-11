from rest_framework import serializers
from occasions.models import Occasion


class OccasionSerializer(serializers.ModelSerializer):
    id = serializers.ReadOnlyField()

    class Meta:
        model = Occasion
        fields = ('id', 'name',)