from rest_framework import routers
from django.urls import path, include

from borrowings.views import BorrowingViewSet

router = routers.DefaultRouter()
router.register("", BorrowingViewSet)

urlpatterns = [
    path("", include(router.urls)),
]

app_name = "borrowings"
