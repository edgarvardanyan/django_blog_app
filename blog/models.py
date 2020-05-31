from django.db import models
from django.utils import timezone
from django.urls import reverse


# Create your models here.
# The Post is something users cam create anf publish
class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)

    def publish(self):
        """Publish the already created post
        """
        self.published_date = timezone.now()
        self.save()

    def approved_comments(self):
        """Returns all the comments of this post that have been approved
        """
        return self.comments.filter(approved_comment=True)

    def get_absolute_url(self):
        return reverse("post_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title

# Post-Comment Relationship is a one-to-many relationship with
# Post.comments and Comment.post being the related names


class Comment(models.Model):
    post = models.ForeignKey('blog.Post',
                             related_name='comments',
                             on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    text = models.TextField()
    create_date = models.DateTimeField(default=timezone.now)
    approved_comment = models.BooleanField(default=False)

    def approve(self):
        """Approve the comment
        """
        self.approved_comment = True
        self.save()

    def get_absolute_url(self):
        return reverse("post_list")

    def __str__(self):
        return self.text
