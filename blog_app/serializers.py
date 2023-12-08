import json

from rest_framework import serializers
from rest_framework.renderers import JSONRenderer

from blog_app.models import Post

# Реализация с автоматическими методами создания и обновления.
# В это варианте методы .create и .update создаются автоматически
class PostSerializer(serializers.ModelSerializer):
    class Meta:
        fields = ('id', 'title', 'body')
        model = Post


# Реализация c методами создания и обновления вручную.
"""class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()
    
    def create(self, validated_data):
        return Post(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.body = validated_data.get('body', instance.body)
        return instance"""




"""class PostModel:
    def __init__(self, title, body):
        self.title = title
        self.body = body


class PostSerializer(serializers.Serializer):
    title = serializers.CharField(max_length=255)
    body = serializers.CharField()


def encode():
    model = PostModel('Световой год', 'Световой год является расстоянием, которое преодолевает свет за один год на земле')
    model_sr = PostSerializer(model)
    print(model_sr.data, type(model_sr.data), sep='\n')
    json = JSONRenderer().render(model_sr.data)
    print(json)"""



