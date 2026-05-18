from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from books.models import Book
from books.serializers import BookListSerializer, BookSerializer

URL = reverse("books:book-list")


def detail_url(book_id):
    return reverse("books:book-detail", kwargs={"pk": book_id})


class BooksApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.book = Book.objects.create(
            title="The Great Gatsby",
            author="F. Scott Fitzgerald",
            cover=Book.CoverType.HARD,
            inventory=5,
            daily_fee=1.50,
        )

    def test_list_books(self):
        res = self.client.get(URL)
        books = Book.objects.all()
        serializer = BookListSerializer(books, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_retrieve_book(self):
        res = self.client.get(detail_url(self.book.id))
        serializer = BookSerializer(self.book)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    def test_create_book(self):
        payload = {
            "title": "To Kill a Mockingbird",
            "author": "Harper Lee",
            "cover": Book.CoverType.SOFT,
            "inventory": 3,
            "daily_fee": 1.00,
        }

        res = self.client.post(URL, payload)

        self.assertEqual(res.status_code, status.HTTP_201_CREATED)
        self.assertTrue(Book.objects.filter(title=payload["title"]).exists())
        book = Book.objects.get(title=payload["title"])
        for key in payload:
            self.assertEqual(getattr(book, key), payload[key])

    def test_update_book(self):
        payload = {
            "title": "The Great Gatsby - Updated",
            "author": "F. Scott Fitzgerald",
            "cover": Book.CoverType.SOFT,
            "inventory": 10,
            "daily_fee": 2.00,
        }
        res = self.client.put(detail_url(self.book.id), payload)
        self.book.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        for key in payload:
            self.assertEqual(getattr(self.book, key), payload[key])

    def test_partial_update_book(self):
        payload = {
            "inventory": 8,
        }
        res = self.client.patch(detail_url(self.book.id), payload)
        self.book.refresh_from_db()

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(self.book.inventory, payload["inventory"])

    def test_delete_book(self):
        res = self.client.delete(detail_url(self.book.id))

        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        self.assertFalse(Book.objects.filter(id=self.book.id).exists())
