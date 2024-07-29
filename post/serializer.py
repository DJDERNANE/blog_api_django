from account.serializer import UserSerializer
from rest_framework import serializers
from .models import Article, Comment


class ArticleSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    class Meta:
        model = Article
        fields = ['id', 'title', 'content', 'published_date', 'user'] 

        extra_kwargs = {
                'title': {'required': True, 'allow_blank': False, 'min_length' : 4 },
                'content': {'required': True, 'allow_blank': False },
                'user': {'read_only': True}  # Make user read-only
            }



class CommentSerializer(serializers.ModelSerializer):
    user = UserSerializer() 
    article = ArticleSerializer()
    class Meta:
        model = Comment
        fields = ['id', 'content', 'published_date', 'user', 'article', 'parent_comment'] 

        extra_kwargs = {
                'content': {'required': True, 'allow_blank': False },
                'user': {'read_only': True}  ,
                'article': {'read_only': True}  ,
                'parent_comment': {'read_only': True}  ,
            }
        

        def get_replies(self, obj):
            replies = Comment.objects.filter(parent=obj)
            return CommentSerializer(replies).data