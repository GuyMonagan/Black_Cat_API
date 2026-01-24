from rest_framework import viewsets
from .models import Review
from .serializers import ReviewSerializer, ReviewCreateSerializer
from rest_framework.permissions import IsAuthenticated
from .permissions import IsOwner, IsLibrarianOrAdmin

from rest_framework.decorators import action
from rest_framework.response import Response
from rest_framework import status


class ReviewViewSet(viewsets.ModelViewSet):
    queryset = Review.objects.all()

    def get_permissions(self):
        if self.action in ['update', 'partial_update', 'destroy']:
            return [IsOwner() | IsLibrarianOrAdmin()]
        elif self.action == 'approve':
            return [IsLibrarianOrAdmin()]
        return [IsAuthenticated()]

    def get_queryset(self):
        user = self.request.user
        if user.role in ['admin', 'librarian']:
            return Review.objects.all()
        return Review.objects.filter(is_approved=True)

    def get_serializer_class(self):
        if self.action in ['create', 'update', 'partial_update']:
            return ReviewCreateSerializer
        return ReviewSerializer

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    @action(detail=True, methods=['post'])
    def approve(self, request, pk=None):
        review = self.get_object()
        if request.user.role not in ['admin', 'librarian']:
            return Response({"detail": "Недостаточно прав"}, status=403)
        review.is_approved = True
        review.save()
        return Response({"detail": "Отзыв одобрен"})
