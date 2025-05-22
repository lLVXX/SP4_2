# core/serializers.py
from rest_framework import serializers
from .models import Box, BoxDeliveryRecord, FinDeTurnoRecord

class BoxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Box
        fields = '__all__'

class BoxDeliverySerializer(serializers.ModelSerializer):
    class Meta:
        model = BoxDeliveryRecord
        fields = '__all__'

class FinDeTurnoSerializer(serializers.ModelSerializer):
    class Meta:
        model = FinDeTurnoRecord
        fields = '__all__'
