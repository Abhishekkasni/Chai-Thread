from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500, blank=True, null=True)
    photo = models.ImageField(upload_to='photos/', blank=True, null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    saved_by = models.ManyToManyField(User, related_name='saved_tweets', blank=True)

    # 🔁 Repost support
    original_tweet = models.ForeignKey(
        'self',
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name='reposts'
    )

    def clean(self):
        if not self.text and not self.photo and not self.video and not self.original_tweet:
            raise ValidationError('A tweet must have either content or be a repost.')

    def is_repost(self):
        return self.original_tweet is not None

    def __str__(self):
        return f'{self.user.username}'

class Comment(models.Model):
    tweet = models.ForeignKey(Tweet, related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    body = models.TextField(max_length=300)
    parent = models.ForeignKey('self', null=True, blank=True, related_name='replies', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        preview = self.body[:30] + '...' if len(self.body) > 30 else self.body
        return f'{self.author.username}: {preview}'

    def is_reply(self):
        return self.parent is not None

