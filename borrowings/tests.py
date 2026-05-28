from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from django.contrib.auth import get_user_model
from freezegun import freeze_time

from books.models import Book
from borrowings.models import Borrowing
from borrowings.serializers import BorrowingListSerializer, BorrowingDetailSerializer

URL = reverse("borrowings:borrowing-list")
USER = get_user_model()


def detail_url(borrowing_id):
    return reverse("borrowings:borrowing-detail", kwargs={"pk": borrowing_id})


def sample_book(**params):
    defaults = {
        "title": "The Great Gatsby",
        "author": "F. Scott Fitzgerald",
        "cover": Book.CoverType.HARD,
        "inventory": 5,
        "daily_fee": 1.50,
    }
    defaults.update(params)

    return Book.objects.create(**defaults)


class PublicBorrowingsApiTests(TestCase):
    def setUp(self):
        self.client = APIClient()
        self.user = USER.objects.create_user(
            email="user@gmail.com", password="userpass"
        )
        self.client.force_authenticate(user=self.user)

    def test_unauthenticated_user_empty_list(self):
        self.client.force_authenticate(user=None)
        res = self.client.get(URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    def test_list_borrowings(self):
        book1 = sample_book()
        book2 = sample_book(title="To Kill a Mockingbird", author="Harper Lee")
        borrowing1 = Borrowing.objects.create(user=self.user, book=book1)
        borrowing2 = Borrowing.objects.create(user=self.user, book=book2)

        res = self.client.get(URL)
        borrowings = Borrowing.objects.filter(user=self.user)
        serializer = BorrowingListSerializer(borrowings, many=True)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)

    @freeze_time("2026-01-01")
    def test_list_borrowings_excludes_returned(self):
        book = sample_book()
        borrowing = Borrowing.objects.create(
            user=self.user, book=book, actual_return_date="2026-02-01"
        )
        res = self.client.get(URL)
        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, [])

    def test_retrieve_borrowing(self):
        book = sample_book()
        borrowing = Borrowing.objects.create(user=self.user, book=book)

        res = self.client.get(detail_url(borrowing.id))
        serializer = BorrowingDetailSerializer(borrowing)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(res.data, serializer.data)
