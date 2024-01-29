from django.urls import path
from . import views


urlpatterns = [
    path('list-create/', views.BlogListCreateAPIView.as_view()),
    path('rud/<int:pk>/', views.BlogRUDAPIView.as_view()),
]
