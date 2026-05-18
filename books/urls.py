from rest_framework import routers
from django.urls import path, include

from books.views import BookViewset

router = routers.DefaultRouter()

router.register("", BookViewset)

urlpatterns = [
    path("", include(router.urls)),
]


app_name = "books"
