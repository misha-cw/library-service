from django.db import models

from config.settings import AUTH_USER_MODEL


class Borrowing(models.Model):
    borrow_date = models.DateField(auto_now_add=True)
    expected_return_date = models.DateField(null=True, blank=True)
    actual_return_date = models.DateField(null=True, blank=True)
    book = models.ForeignKey(
        "books.Book", on_delete=models.CASCADE, related_name="borrowings"
    )
    user = models.ForeignKey(
        AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="borrowings"
    )

    class Meta:
        ordering = ["-borrow_date"]
        constraints = [
            models.CheckConstraint(
                condition=models.Q(expected_return_date__gte=models.F("borrow_date")),
                name="expected_return_date_after_borrow_date",
            ),
            models.CheckConstraint(
                condition=models.Q(actual_return_date__gte=models.F("borrow_date")),
                name="actual_return_date_after_borrow_date",
            ),
        ]

    def __str__(self):
        return (
            f"Borrowing #{self.pk} (User ID: {self.user_id}, Book ID: {self.book_id})"
        )
