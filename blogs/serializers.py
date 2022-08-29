from rest_framework import serializers
from .models import ArticleImageModel, ArticleModel, CommentModel
from .messages import Messages
from django.conf import settings
from django.db import transaction, DatabaseError
from rest_framework.exceptions import NotAcceptable
from rest_framework.serializers import SerializerMethodField


class ArticleSerializer(serializers.ModelSerializer):
    """
        This class used to serialize input data for create Article
    """

    images = serializers.ListField(required=False,
        child=serializers.ImageField(use_url=True), max_length=settings.MAX_IMAGES_LENGTH)
    author = serializers.ReadOnlyField(source='author.username')
    comments = SerializerMethodField()
    
    class Meta:
        model = ArticleModel
        fields = ('id', 'title', 'body', 'author', 'images', 'comments')

    def validate_images(self, value):
        error = {}
        for image in value:
            if image.size > settings.MAX_IMAGE_SIZE:
                error[image.name] = Messages.IMAGE_SIZE.value
            if error:
                raise serializers.ValidationError(error)
        return value

    def create(self, validated_data):
        images = validated_data.pop('images', False)
        try:
            with transaction.atomic():
                article_obj = super().create(validated_data)
                if images:
                    ArticleImageModel.objects.bulk_create(
                        ArticleImageModel(
                            article = article_obj,
                            image = picture
                        )for picture in images
                )
        except DatabaseError:
            raise NotAcceptable(Messages.DATABASE_ERROR.value)
        return article_obj
    def get_comments(self, obj):
        result = obj.comments.all()
        return CommentSerializer(instance=result, many=True).data
                    
class CommentSerializer(serializers.ModelSerializer):
    """
        This class used to serialize input data for create comment
    """
    class Meta:
        model = CommentModel
        fields = ('user', 'text')

