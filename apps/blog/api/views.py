from rest_framework import generics, viewsets, permissions, status
from . import serializers
from ..models import Blog
from .permissions import IsAdminOrReadOnly, IsOwnerOrReadOnly


class BlogListCreateAPIView(generics.ListCreateAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsAdminOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.BlogGetSerializer
        return serializers.BlogPostSerializer


class BlogRUDAPIView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Blog.objects.all()
    permission_classes = [IsOwnerOrReadOnly]

    def get_serializer_class(self):
        if self.request.method == 'GET':
            return serializers.BlogGetSerializer
        return serializers.BlogPostSerializer
