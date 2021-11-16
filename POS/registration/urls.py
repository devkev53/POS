from django.urls import path
from django.contrib.auth import views as auth_views
from .views import UserListView, UserCreateView,ProfileCreate

urlpatterns = [
    path('login/', auth_views.LoginView.as_view
    (template_name = 'registration/login.html'), name='login'),
    path('logout', auth_views.LogoutView.as_view
    (template_name = 'registration/login.html'), name='logout'),
    path('users-list/', UserListView.as_view(), name='users-list'),
    path('users-new/', ProfileCreate.as_view(), name='users-new'),
]