from rest_framework import viewsets
from .models import Event 
from .serializers import EventSerializer 
from users.permissions import IsManager


class EventViewSet(viewsets.ModelViewSet):
    queryset = Event.objects.all()
    serializer_class = EventSerializer 
    permission_classes = [IsManager]

