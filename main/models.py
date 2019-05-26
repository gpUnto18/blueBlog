from django.db import models
from django.utils import timezone
from django.core.exceptions import ValidationError

class Post(models.Model):
    author = models.ForeignKey('auth.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=200)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)
    published_date = models.DateTimeField(blank=True, null=True)
    image = models.ImageField(upload_to='image/', blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Me(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    image = models.ImageField(upload_to='image/', blank=True, null=True)

    def save(self, *args, **kwargs):
        if Me.objects.exists() and not self.pk:
          raise ValidationError('Only one entry allowed.')
        return super(Me, self).save(*args, **kwargs)

    def __str__(self):
        return self.name

class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    author = models.CharField(max_length=200)
    title = models.CharField(max_length=200)
    text = models.TextField()
    published_date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return self.title + ', ' + self.author

class Info(models.Model):
    title = models.CharField(max_length=200)
    text = models.TextField()

    def __str__(self):
        return self.title

class Link(models.Model):
    name = models.CharField(max_length=200)
    link = models.URLField(max_length=200)

    def __str__(self):
        return self.name

class GalleryImage(models.Model):
    title = models.CharField(max_length=200, default="")
    created_date = models.DateTimeField(default=timezone.now)
    image = models.ImageField(upload_to='image/', blank=False, null=False)

    def __str__(self):
        return self.title

class AdminLoginAttempts(models.Model):
    group = models.IntegerField()
    attempts = models.IntegerField()
    lastTime = models.DateTimeField(default=timezone.now)
