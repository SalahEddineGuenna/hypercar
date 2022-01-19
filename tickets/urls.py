from django.urls import path
from .views import WelcomeView, MenuView, QueueHandler, ProcessQueue, NextTicket
from django.views.generic.base import RedirectView

urlpatterns = [
    path('welcome/', WelcomeView.as_view()),
    path('menu/', MenuView.as_view(), name="menu"),
    path('get_ticket/<link>/', QueueHandler.as_view()),
    path('processing', ProcessQueue.as_view()),
    path('processing/', RedirectView.as_view(url='/processing')),
    path('next', NextTicket.as_view()),
]
