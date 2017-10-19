from rest_framework import serializers
from .models import Result, District, Voivodeship, Constituency, Commune


class VoivSerializer(serializers.ModelSerializer):
    class Meta:
        model = Voivodeship
        fields = ('pk', 'name', 'abr')
