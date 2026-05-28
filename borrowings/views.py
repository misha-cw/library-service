from rest_framework import generics, viewsets

from borrowings.models import Borrowing
from borrowings.serializers import (
    BorrowingSerializer,
    BorrowingListSerializer,
    BorrowingDetailSerializer,
)


class BorrowingReadOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Borrowing.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BorrowingListSerializer
        return BorrowingDetailSerializer

    def get_queryset(self):
        user = self.request.user
        if user.is_authenticated:
            return Borrowing.objects.filter(user=user, actual_return_date__isnull=True)
        return Borrowing.objects.none()
