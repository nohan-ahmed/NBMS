from django.urls import path
from . import views
urlpatterns = [
    path('borrow/<int:pk>/', views.BorrowView.as_view(), name="borrow_now"),
    path('return/<int:pk>/', views.ReturnView.as_view(), name="return_now"),
]
