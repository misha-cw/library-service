from rest_framework import serializers

from borrowings.models import Borrowing
from books.serializers import BookSerializer, BookListSerializer


class BorrowingSerializer(serializers.ModelSerializer):
    class Meta:
        model = Borrowing
        fields = (
            "id",
            "borrow_date",
            "expected_return_date",
            "actual_return_date",
            "book",
        )
        read_only_fields = ("id", "borrow_date")


class BorrowingListSerializer(BorrowingSerializer):
    book = BookListSerializer(read_only=True)


class BorrowingDetailSerializer(BorrowingSerializer):
    book = BookSerializer(read_only=True)
