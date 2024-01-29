from rest_framework import serializers
from .. import models
from apps.account.api.serializers import AccountUpdateSerializer
from apps.main.api.serializers import CategorySerializer, TagSerializer


class BlogGetSerializer(serializers.ModelSerializer):
    author = AccountUpdateSerializer(read_only=True)
    category = CategorySerializer(read_only=True)
    tags = TagSerializer(read_only=True, many=True)

    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'author', 'category', 'tags', 'views', 'image', 'created_date', 'modified_date']


class BlogPostSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Blog
        fields = ['id', 'title', 'author', 'category', 'tags', 'image']
        extra_kwargs = {
            'author': {'required': False},
            'image': {'required': False},
        }

    def create(self, validated_data):
        request = self.context.get('request')
        tags = validated_data.pop('tags')
        author_id = request.user.id
        obj = models.Blog.objects.create(author_id=author_id, **validated_data)
        if tags:
            for tag in tags:
                obj.tags.add(tag)
        return obj

    def update(self, instance, validated_data):
        tags = validated_data.pop('tags', None)
        input_tags = set(tags)
        current_tags = set(instance.tags.all())
        to_remove_tags = current_tags.difference(input_tags)
        to_add_tags = input_tags.difference(current_tags)
        if to_remove_tags:
            for tag in to_remove_tags:
                instance.tags.remove(tag)
        if to_add_tags:
            for tag in to_add_tags:
                instance.tags.add(tag)
        return super().update(instance, validated_data)


class CommentGETSerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Comment
        fields = ['id', 'author', 'parent_comment', 'blog', 'body', 'created_date', 'top_level_comment_id']
