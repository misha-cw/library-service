from rest_framework import generics, viewsets, mixins

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingCreateSerializer,
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingViewSet(
    mixins.CreateModelMixin,
    mixins.ListModelMixin,
    mixins.RetrieveModelMixin,
    viewsets.GenericViewSet,
):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        if self.action == "retrieve":
            return BorrowingDetailSerializer
        if self.action == "create":
            return BorrowingCreateSerializer
        return BorrowingSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Borrowing.objects.filter(user=user, actual_return_date__isnull=True)
        return Borrowing.objects.none()

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
