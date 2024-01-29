from django.urls import path, include
from . import views
from rest_framework.routers import DefaultRouter

router_category = DefaultRouter()
router_category.register('category', views.CategoryViewSet)
router_tag = DefaultRouter()
router_tag.register('tag', views.TagViewSet)


urlpatterns = [
    path('', include(router_category.urls)),
    path('', include(router_tag.urls)),
    path('subscribe/', views.SubscribeListCreateView.as_view()),
]
