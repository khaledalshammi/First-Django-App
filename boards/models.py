from django.db import models
from django.contrib.auth.models import User
from django.utils.text import Truncator
class Board(models.Model):
    name = models.CharField(max_length=50,unique=True)
    description = models.CharField(max_length=150)
    def __str__(self):
        return self.name
    def get_p_c(self):
        return Post.objects.filter(topic__board=self).count()
    def get_last(self):
        return Post.objects.filter(topic__board=self).order_by('-created_dt').first()




class Topic(models.Model):
    subject = models.CharField(max_length=255)
    board = models.ForeignKey(Board,related_name='topics',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='topics',on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    views = models.PositiveIntegerField(default=0)
    up_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    up_dt = models.DateTimeField(null=True)
    def __str__(self) -> str:
        return self.subject



        
class Post(models.Model):
    message = models.TextField(max_length=4000)
    topic = models.ForeignKey(Topic,related_name='posts',on_delete=models.CASCADE)
    created_by = models.ForeignKey(User,related_name='posts',on_delete=models.CASCADE)
    created_dt = models.DateTimeField(auto_now_add=True)
    up_by = models.ForeignKey(User,null=True,on_delete=models.CASCADE)
    up_dt = models.DateTimeField(null=True)
    def __str__(self) -> str:
        t = Truncator(self.message)
        return t.chars(24)