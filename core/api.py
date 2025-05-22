# core/api.py
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Box, BoxDeliveryRecord, FinDeTurnoRecord
from .serializers import BoxSerializer, BoxDeliverySerializer, FinDeTurnoSerializer

class BoxViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Box.objects.all()
    serializer_class = BoxSerializer
    permission_classes = [IsAuthenticated]

class BoxDeliveryViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = BoxDeliveryRecord.objects.all()
    serializer_class = BoxDeliverySerializer
    permission_classes = [IsAuthenticated]

class FinDeTurnoViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = FinDeTurnoRecord.objects.all()
    serializer_class = FinDeTurnoSerializer
    permission_classes = [IsAuthenticated]
