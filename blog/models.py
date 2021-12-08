from django.db import models
from django.conf import settings
from django.db.models.deletion import CASCADE
from django.db.models.expressions import Case
from django.utils import timezone
from django.urls import reverse
from ckeditor_uploader.fields import RichTextUploadingField
from taggit.managers import TaggableManager

# creating model Manager


class PublishedManager(models.Manager):
    def get_queryset(self):
        return super(PublishedManager, self).get_queryset().filter(status=1)


STATUS = (
    (0, "Draft"),
    (1, "Published")
)

# post model


class Post(models.Model):
    title = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(max_length=200, unique_for_date='publish')
    author = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='blog_posts')
    image = models.ImageField(upload_to='featured_image/%Y/%m/%d/')
    body = RichTextUploadingField()

    publish = models.DateTimeField(default=timezone.now)
    updated_on = models.DateTimeField(auto_now=True)
    created_on = models.DateTimeField(auto_now_add=True)
    status = models.IntegerField(choices=STATUS, default=0)
    tags = TaggableManager()

    objects = models.Manager()  # default manager
    published = PublishedManager()  # Custom manager

    class Meta:
        ordering = ['-publish', ]

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("blog:post_detail", args=[self.slug])

    def get_comments(self):
        return self.comments.filter(parent=None).filter(active=True)

# comment model


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=CASCADE, related_name='comments')
    name = models.CharField(max_length=50)
    email = models.EmailField()
    parent = models.ForeignKey(
        "self", null=True, blank=True, on_delete=CASCADE)
    body = models.TextField()

    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)

    class Meta:
        ordering = ('created',)

    def __str__(self):
        return self.body

    def get_comments(self):
        return Comment.objects.filter(parent=self).filter(active=True)
