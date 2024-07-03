from django.urls import path
from . import views
urlpatterns = [
    path('detail/<slug:slug>?<int:id>/', views.DetailBook.as_view(), name='detail_book')
]
