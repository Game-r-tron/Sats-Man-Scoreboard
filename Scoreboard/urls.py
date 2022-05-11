from django.urls import path, include
from . import views
from .views import (
    ScoreboardApiView,
)

urlpatterns = [
    path('', views.index, name='index'),
    path('api', ScoreboardApiView.as_view()),
]