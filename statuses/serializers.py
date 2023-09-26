from .models import StatusModel, StatusLikeModel, StatusCommentModel
from rest_framework import serializers


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusModel
        fields = '__all__'
        read_only_fields = ['created']


class StatusCommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusCommentModel
        fields = '__all__'
        read_only_fields = ['created', 'user']


class StatusLikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = StatusLikeModel
        fields = '__all__'
        read_only_fields = ['user']
