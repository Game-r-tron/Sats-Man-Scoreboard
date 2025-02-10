from django.urls import path, include
from . import views
from .views import (
    ScoreboardApiView,
    ZBDAPIView,
    PaidAPIView,
    PaymentCheckAPIView,
    game_view,
)

import datetime
current_year = datetime.date.today().isocalendar()[0]
current_week = datetime.date.today().isocalendar()[1]

urlpatterns = [
    path('', views.date, {'year':current_year, 'week':current_week}, name='date'),
    path('top/<int:top>/', views.top, name='top'),
    path('event/<str:event>/', views.event, name='event'),
    path('event/<str:event>/top/<int:top>/', views.eventtop, name='eventtop'),
    path('date/<int:year>/<int:week>/', views.date, name='date'),
    path('date/<int:year>/<int:week>/top/<int:top>/', views.datetop, name='datetop'),
    path('all', views.all, name='all'),
    path('api', ScoreboardApiView.as_view()),
    path('zbd', ZBDAPIView.as_view()),
    path('enter-details/<str:score_id>', views.enter_details, name='score_id'),
    path('enter-details/<str:score_id>/<str:event_code>', views.enter_details_event, name='score_id_event'),
    path('payment-made', PaidAPIView.as_view()),
    path('payment-check', PaymentCheckAPIView.as_view()),
    path('game/', game_view, name='game'),
]