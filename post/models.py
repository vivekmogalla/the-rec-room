import uuid

from django.db import models
from django.utils.timesince import timesince

from account.models import User

class Like(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='likes', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    body = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, related_name='comments', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return "Comment by {} on {}".format(self.created_by, self.created_at)


class Save(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    created_by = models.ForeignKey(User, related_name='saved_recs', null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)


class PostAttachment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    image = models.ImageField(upload_to='post_attachments')
    created_by = models.ForeignKey(User, related_name='post_attachments', on_delete=models.CASCADE)


class Genre(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=255)

    class Meta:
        ordering = ('name',)
        
    def __str__(self):
        return self.name


def get_media_type():
    return MediaType.objects.get_or_create(name="Media")[0]

def get_media_type_id():
    return get_media_type().id
    
class MediaType(models.Model):
    name = models.CharField(max_length=50, unique=True)
    icon = models.CharField(max_length=30, blank=True)
    genres = models.ManyToManyField(Genre, related_name='media_types', symmetrical=False, blank=True)

    def __str__(self):
        return self.name


class Post(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    title = models.CharField(max_length=255, blank=True, null=True)
    body = models.TextField(blank=True, null=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    created_by = models.ForeignKey(User, related_name='posts', on_delete=models.CASCADE)
    
    recipients = models.ManyToManyField(User, related_name='received_recs', symmetrical=False, blank=True)

    media_type = models.ForeignKey(MediaType, related_name='posts', on_delete=models.SET(get_media_type), default=get_media_type_id)
    
    genres = models.ManyToManyField(Genre, related_name='posts', symmetrical=False, blank=True)

    attachments = models.ManyToManyField(PostAttachment, blank=True)
    link = models.URLField(max_length=255, blank=True, null=True)
    # SARAH: add link model
    # link_data = models.JSONField()
    
    likes = models.ManyToManyField(Like, blank=True)
    likes_count = models.IntegerField(default=0)

    comments = models.ManyToManyField(Comment, blank=True)
    comments_count = models.IntegerField(default=0)

    saved_recs = models.ManyToManyField(Save, blank=True)
    # IMPORTANT: should this be changed???? Solution above is currently very complex
    # saved_by = models.ForeignKey(User, related_name="saved_recs", symmetrical=False, blank=True)
    saves_count = models.IntegerField(default=0)

    class Meta:
        ordering = ('-created_at',)
        # abstract = True

    def __str__(self):
        return (
            f"{self.created_by} "
            f"({self.created_at:%y-%m-%d %H:%M}): "
            f"{self.title}"
        )

    def created_at_formatted(self):
       return timesince(self.created_at)

# SARAH: If we use these, won't need MediaType anymore
# class Book(Post):
#     author = models.CharField(max_length=255, blank=True)
# class Film(Post):
#     director = models.CharField(max_length=255, blank=True)
# class Music(Post):
#     artist = models.CharField(max_length=255, blank=True)
#     album = models.CharField(max_length=255, blank=True)
# class Show(Post):
#     director = models.CharField(max_length=255, blank=True)


class Trend(models.Model):
    hashtag = models.CharField(max_length=255)
    occurrences = models.IntegerField()


class Report(models.Model):
    THREATS = 'threats'
    HARASSMENT = 'harassment'
    PORNOGRAPHY = 'pornography'
    SPAM = 'spam'
    PRIVACY = 'privacy'
    COPYRIGHT = 'copyright'
    TERMS = 'terms'
    OTHER = 'other'

    CHOICES_TYPE_OF_REPORT = (
        (THREATS, 'Threats of violence'),
        (HARASSMENT, 'Harassment'),
        (PORNOGRAPHY, 'Pornographic content'),
        (SPAM, 'Spam'),
        (PRIVACY, 'Privacy violation'),
        (COPYRIGHT, 'Copyright violation'),
        (TERMS, 'Terms of Service violation'),
        (OTHER, 'Other'),
    )

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    post = models.ForeignKey(Post, related_name='reports', blank=True, null=True, on_delete=models.SET_NULL)
    comment = models.ForeignKey(Comment, related_name='reports', blank=True, null=True, on_delete=models.SET_NULL)
    type_of_report = models.CharField(max_length=50, choices=CHOICES_TYPE_OF_REPORT, default=OTHER)
    body = models.CharField(max_length=255, blank=True, null=True)
    addressed = models.BooleanField(default=False)
    created_by = models.ForeignKey(User, related_name='reports', blank=True, null=True, on_delete=models.SET_NULL)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ('created_at',)

    def __str__(self):
        return (
            f"{self.get_type_of_report_display()} report made on "
            f"{self.created_at:%y-%m-%d %H:%M}"
        )
