from django.db import models
from django.contrib.auth import get_user_model
import uuid
from datetime import datetime

from tinymce.models import HTMLField

from io import BytesIO
from PIL import Image
from django.core.files import File

User = get_user_model()
# Create your models here.

def compress(image):
    im = Image.open(image)
    im_io = BytesIO()
    im.save(im_io, 'JPEG', quality=60)
    new_image = File(im_io, name=image.name)
    return new_image

class Profile(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    id_user = models.IntegerField()
    bio = models.TextField(blank=True)
    profileimg = models.ImageField(upload_to='profile_images', default='blank-profile-picture.png')
    location = models.CharField(max_length=100, blank=True)
    first_name = models.CharField(max_length=100, blank=True)
    last_name = models.CharField(max_length=100, blank=True)
    email = models.CharField(max_length=100, blank=True)
    verified_email = models.BooleanField(default=False)
    gender = models.CharField(max_length=10, blank=True)
    birth_date = models.CharField(max_length=100, blank=True)
    
    def save(self, *args, **kwargs):
        new_image = compress(self.profileimg)
        self.profileimg = new_image
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.user.username

class Article(models.Model):
    title = models.CharField(max_length=255)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    category = models.CharField(max_length=50)
    subtitle = models.CharField(max_length=255)
    cover_image = models.ImageField(upload_to='cover_images')
    content = HTMLField()
    is_draft = models.BooleanField(default=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateField(auto_now_add=True)
    author_profile = models.ForeignKey(Profile, on_delete=models.CASCADE, related_name='authored_articles', default=None, null=True)
    no_of_like = models.IntegerField(default=0)
    
    def save(self, *args, **kwargs):
        new_image = compress(self.profileimg)
        self.profileimg = new_image
        super().save(*args, **kwargs)
    
    def __str__(self):
        return self.title
   
class Type(models.Model):
    type = models.CharField(max_length=15)
    
    def __str__(self):
        return self.type

class Category(models.Model):
    category = models.CharField(max_length=20)
    
    def __str__(self):
        return self.category   
   
    
class Literature(models.Model):
    title = models.CharField(max_length=500)
    author = models.CharField(max_length=60)
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    source_url = models.CharField(max_length=1000)
    type = models.ForeignKey(Type, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    cover_image = models.ImageField(upload_to='literature_covers')
    description = models.TextField()
    access_frequency = models.IntegerField(default=0)
    
    def __str__(self):
        return self.title
    
class Note(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    title = models.CharField(max_length=250)
    note = models.TextField()
    date = models.DateField(auto_now_add=True)
    
    def __str__(self):
        return self.title
    
class Comment(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4)
    commentator = models.ForeignKey(User, on_delete=models.CASCADE)
    commentator_profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    commented_article = models.ForeignKey(Article, on_delete=models.CASCADE)
    comment = models.TextField()
    
    def __str__(self):
        return self.comment
    
class FollowersCount(models.Model):
    follower = models.CharField(max_length=1000)
    user = models.CharField(max_length=1000)
    
    def __str__(self):
        return f"{self.follower} following {self.user}"
    
class LikeArticle(models.Model):
    article_id = models.CharField(max_length=200)
    username = models.CharField(max_length=150)
    
    def __str__(self):
        return f"{self.username} like on {self.article_id}"
    
class Testmigrate(models.Model):
    stringtes = models.CharField(max_length=200)
    
    def __str__(self):
        return self.stringtes