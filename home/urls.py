
from django.urls import path
from .views import LandingPageView

app_name = 'home'

urlpatterns = [
    path('', LandingPageView.as_view(), name='home'),
]
