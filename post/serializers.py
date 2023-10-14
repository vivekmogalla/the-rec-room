from .models import Post, Comment, Like, Save, Trend, MediaType, Genre
from account.serializers import UserSerializer
from rest_framework import serializers

class LikeSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Like 
        fields = ('id', 'created_by',)

class SaveSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)

    class Meta:
        model = Save 
        fields = ('id', 'created_by',)

class GenreSerializer(serializers.ModelSerializer):
    class Meta:
        model = Genre
        fields = ('id', 'name',)

class MediaTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = MediaType
        fields = ('id', 'name', 'icon', 'genres',)

class PostSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    recipients = UserSerializer(read_only=True, many=True)
    genres = GenreSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format='%b %d, %Y %I:%M%p')
    likes = LikeSerializer(read_only=True, many=True)
    saved_recs = SaveSerializer(read_only=True, many=True)
    media_type = MediaTypeSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes', 'likes_count', 'saved_recs', 'saves_count', 'comments_count', 'created_by', 'created_at', 'created_at_formatted', 'media_type', 'recipients', 'genres', 'title', 'link',)

class CommentSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    created_at = serializers.DateTimeField(format='%b %d, %Y %I:%M%p')

    class Meta:
        model = Comment
        fields = ('id', 'body', 'created_by', 'created_at',)

class PostDetailSerializer(serializers.ModelSerializer):
    created_by = UserSerializer(read_only=True)
    recipients = UserSerializer(read_only=True, many=True)
    genres = GenreSerializer(read_only=True, many=True)
    created_at = serializers.DateTimeField(format='%b %d, %Y %I:%M%p')
    comments = CommentSerializer(read_only=True, many=True)
    media_type = MediaTypeSerializer(read_only=True)

    class Meta:
        model = Post
        fields = ('id', 'body', 'likes_count', 'comments_count', 'saves_count', 'created_by', 'created_at', 'comments', 'media_type', 'recipients', 'genres', 'title', 'link',)

class TrendSerializer(serializers.ModelSerializer):
    class Meta:
        model = Trend
        fields = ('id', 'hashtag', 'occurrences',)