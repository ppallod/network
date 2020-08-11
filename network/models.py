from django.contrib.auth.models import AbstractUser
from django.db import models
from django.core.exceptions import ValidationError


class User(AbstractUser):
    pass

class Post(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="posts")
    text = models.CharField(max_length=1024)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.id} by {self.user.username}"
    
    @property
    def total_likes(self):
        return self.likes.count()
    
    @property 
    def has_liked(self, request):
        user = request.user
        like = Like.objects.filter(post=self, user=user)
        if like is not None:
            return False
        else:
            return True


class Like(models.Model):
    class Meta:
        unique_together = ('user', 'post')

    id = models.AutoField(primary_key=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name="likes")
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Post {self.post.id} liked by {self.user.username}"

class Follower(models.Model):
    id = models.AutoField(primary_key=True)
    follower = models.ForeignKey(User, on_delete=models.CASCADE, related_name="following")
    following = models.ForeignKey(User, on_delete=models.CASCADE, related_name="followers")
    timestamp = models.DateTimeField(auto_now_add=True)

    def save(self,*args, **kwargs):
        if self.follower.id != self.following.id:
            super(Follower,self).save(*args, **kwargs)
        else:
            raise ValidationError("A user cannot follow himself")


    def __str__(self):
        return f"{self.follower.username} following {self.following.username}"

