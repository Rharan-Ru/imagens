from django.urls import path
from .views import ImagemView

urlpatterns = [
    path('', ImagemView.as_view()),
]
