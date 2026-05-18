from rest_framework import viewsets

from books.models import Book
from books.serializers import BookListSerializer, BookSerializer


class BookViewset(viewsets.ModelViewSet):
    serializer_class = BookSerializer
    queryset = Book.objects.all()

    def get_serializer_class(self):
        if self.action == "list":
            return BookListSerializer
        return BookSerializer
