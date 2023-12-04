from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(Article)
admin.site.register(Literature)
admin.site.register(Type)
admin.site.register(Category)
admin.site.register(Note)
admin.site.register(Comment)
admin.site.register(FollowersCount)
admin.site.register(LikeArticle)