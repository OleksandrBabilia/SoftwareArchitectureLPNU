from rest_framework import viewsets
from .models import Depository
from .serializers import DepositorySerializer
from users.permissions import IsManager


class DepositoryViewSet(viewsets.ModelViewSet):
    queryset = Depository.objects.all()
    serializer_class = DepositorySerializer 
    permission_classes = [IsManager]

