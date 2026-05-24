from rest_framework import routers
from django.urls import path, include

from borrowings.views import BorrowingReadOnlyViewSet

router = routers.DefaultRouter()
router.register("", BorrowingReadOnlyViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowings"
