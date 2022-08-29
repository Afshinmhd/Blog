from django.contrib import admin
from .models import ArticleImageModel, ArticleModel, CommentModel


admin.site.register(ArticleImageModel)
admin.site.register(ArticleModel)
admin.site.register(CommentModel)