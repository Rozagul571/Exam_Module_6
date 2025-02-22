from django.urls import path
from apps.views import RegisterFormView, VerifyFormView, LoginView, LogoutView, UserProfileListView, \
    TransactionListView, UserProfileUpdateView

urlpatterns = [
    path('register/', RegisterFormView.as_view(), name='register'),
    path('verify/', VerifyFormView.as_view(), name='verify_gmail'),
    path('login/', LoginView.as_view(), name='login'),

    path('profile', UserProfileListView.as_view(), name='profile'),

    path('edit_profile/', UserProfileUpdateView.as_view(), name='edit_profile'),
    path('transactions/', TransactionListView.as_view(), name='transactions'),
    path('logout/', LogoutView.as_view(), name='logout'),
]