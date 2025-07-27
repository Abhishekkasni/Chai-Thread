from django.db import models
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
# Create your models here.

class Tweet(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.TextField(max_length=500,blank=True, null=True)
    photo = models.ImageField(upload_to='photos/',blank=True,null=True)
    video = models.FileField(upload_to='videos/', blank=True, null=True) 
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def clean(self):
        if not self.text and not self.photo and not self.video:
            raise ValidationError('A tweet must have either text, a photo, or a video.')

    def __str__(self):
        return f'{self.user.username} - {self.text[:10]}'
    
    