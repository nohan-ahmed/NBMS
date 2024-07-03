from django.urls import path
from core.views import HomeView
urlpatterns = [
    path('<slug:slug>/', HomeView.as_view(), name='category')
]
