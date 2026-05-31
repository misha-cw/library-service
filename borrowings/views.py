from rest_framework import generics, viewsets, mixins
from rest_framework.permissions import IsAuthenticated

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
    permission_classes = (IsAuthenticated,)

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
        queryset = Borrowing.objects.all()
        if user.is_staff:
            user_id = self.request.query_params.get("user_id")
            if user_id:
                queryset = queryset.filter(user_id=user_id)
        else:
            queryset = queryset.filter(user=user)

        is_active = self.request.query_params.get("is_active")

        if is_active:
            queryset = queryset.filter(actual_return_date__isnull=True)

        return queryset

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)
