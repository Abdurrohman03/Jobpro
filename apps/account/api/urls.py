from django.urls import path
from . import views


urlpatterns = [
    path('register/', views.AccountRegisterView.as_view()),
    path('login/', views.LoginView.as_view()),
    path('', views.AccountView.as_view()),
    path('update/<int:pk>/', views.AccountRetrieveUpdateView.as_view()),
    path('image/update/<int:pk>/', views.AccountOwnImageUpdateView.as_view()),
    path('list/', views.AccountListView.as_view()),
    path('set-password/', views.SetNewPasswordView.as_view()),
]
