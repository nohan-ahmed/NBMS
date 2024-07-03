from django.urls import path
from . import views
from django.contrib.auth.views import PasswordChangeView
from django.urls import reverse_lazy

urlpatterns = [
    path('register/', views.RegisterView.as_view(), name='register'),
    path('login/', views.UserLoginView.as_view(), name='login'),
    path('logout/', views.UserLogoutView, name='logout'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('profile/update/', views.ProfileUpdateView.as_view(), name='profile_update'),
    path('profile/deposite/', views.DepositeView.as_view(), name='deposite'),
    path('profile/password-change/', PasswordChangeView.as_view(template_name='./accounts/password_change_form.html', success_url=reverse_lazy('profile')), name='password_change'),

]
