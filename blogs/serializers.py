from rest_framework import serializers
from .models import ArticleImageModel, ArticleModel
from .messages import Messages
from django.conf import settings
from django.db import transaction, DatabaseError
from rest_framework.exceptions import NotAcceptable


class ArticleSerializer(serializers.ModelSerializer):
    """
        This class used to serialize input data for create Article
    """

    images = serializers.ListField(required=False,
        child=serializers.ImageField(use_url=True), max_length=settings.MAX_IMAGES_LENGTH)
    author = serializers.ReadOnlyField(source='author.username')
    
    class Meta:
        model = ArticleModel
        fields = ('title', 'body', 'author', 'images')

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
                    
