from django.db import models
from user.models import User

class Blog(models.Model):

    STATUS_CHOICES = [
        ('draft', 'Draft'),
        ('published', 'Published'),
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    img = models.ImageField(upload_to='blog_images/', null=True, blank=True)
    category = models.CharField(max_length=100, default='general')
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='draft')
    tags = models.CharField(max_length=200, blank=True, default='')
    views = models.IntegerField(default=0)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='blogs')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.title
    
    @property
    def like_count(self):
        return self.likes.count()
    
    @property
    def comment_count(self):
        return self.comments.count()


class Like(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='likes')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_likes')
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('blog', 'user')


class Comment(models.Model):
    blog = models.ForeignKey(Blog, on_delete=models.CASCADE, related_name='comments')
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='blog_comments')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Comment by {self.user.name} on {self.blog.title}"
