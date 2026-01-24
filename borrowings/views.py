from rest_framework import viewsets
from .models import Borrowing
from .serializers import BorrowingSerializer, BorrowingCreateSerializer
from users.permissions import IsReader, IsLibrarianOrAdmin
from rest_framework.permissions import IsAuthenticated
from django_filters.rest_framework import DjangoFilterBackend


class BorrowingViewSet(viewsets.ModelViewSet):
    queryset = Borrowing.objects.all()
    permission_classes = [IsAuthenticated]

    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['book', 'is_returned']

    def get_queryset(self):
        user = self.request.user
        if user.role == 'reader':
            return Borrowing.objects.filter(user=user)
        return Borrowing.objects.all()

    def get_permissions(self):
        if self.action in ['create']:
            return [IsReader()]
        elif self.action in ['update', 'partial_update', 'destroy']:
            return [IsLibrarianOrAdmin()]
        return [IsAuthenticated()]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return BorrowingCreateSerializer
        return BorrowingSerializer
