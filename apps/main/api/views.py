from rest_framework import generics, viewsets, permissions, status
from . import serializers
from .. import models
from .permissions import IsAdminOrReadOnly


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = models.Category.objects.all()
    serializer_class = serializers.CategorySerializer
    permission_classes = [IsAdminOrReadOnly]


class TagViewSet(viewsets.ModelViewSet):
    queryset = models.Tag.objects.all()
    serializer_class = serializers.TagSerializer
    permission_classes = [IsAdminOrReadOnly]


class SubscribeListCreateView(generics.ListCreateAPIView):
    queryset = models.Subscribe.objects.all()
    serializer_class = serializers.SubscribeSerializer


class ContactViewSet(viewsets.ModelViewSet):
    queryset = models.Contact.objects.all()
    serializer_class = serializers.ContactSerializer

