from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from .models import Publisher
from .serializers import PublisherSerializer


class PublisherViewSet(viewsets.ModelViewSet):
    queryset = Publisher.objects.all()
    serializer_class = PublisherSerializer
    # permission_classes = [IsAuthenticated]

