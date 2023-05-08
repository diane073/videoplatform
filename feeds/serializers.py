from feeds.models import Feed
from rest_framework import serializers

class FeedDetailSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()
    comments_count = serializers.SerializerMethodField()
    likes_count = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.email  #Feed, author의 email값

    def get_comments_count(self, obj):
        return obj.comments.count()

    def get_likes_count(self, obj):
        return obj.likes.count()
    
    class Meta:
        model = Feed
        fields = ['title','context', 'image','video', 'created_at', 'updated_at', 'user', "comments_count", "likes_count",]



class FeedListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = '__all__'

class FeedCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Feed
        fields = ['title','context', 'image','video',]

