from .models import PostModel, PostCommentModel, PostEmojiModel, CommentEmojiModel
from rest_framework import serializers


class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostModel
        fields = '__all__'
        read_only_fields = ['created', 'numbers_of_seen', 'user']


class PostCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostCommentModel
        fields = '__all__'
        read_only_fields = ['created', 'user']


class PostEmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = PostEmojiModel
        fields = '__all__'
        read_only_fields = ['user', 'post']


class CommentEmojiSerializer(serializers.ModelSerializer):
    class Meta:
        model = CommentEmojiModel
        fields = '__all__'
        read_only_fields = ['comment', 'post']

