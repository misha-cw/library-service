from rest_framework import serializers
from django.db import transaction

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


class BorrowingCreateSerializer(BorrowingSerializer):
    class Meta(BorrowingSerializer.Meta):
        fields = BorrowingSerializer.Meta.fields + ("user",)
        read_only_fields = BorrowingSerializer.Meta.read_only_fields + ("user",)

    def validate(self, attrs):
        book = attrs.get("book")
        if book and book.inventory <= 0:
            raise serializers.ValidationError("This book is currently unavailable.")
        return attrs

    def create(self, validated_data):
        with transaction.atomic():
            book = validated_data.get("book")
            if book:
                book.inventory -= 1
                book.save()
            return super().create(validated_data)
