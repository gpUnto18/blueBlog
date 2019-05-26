from django.contrib import admin
from .models import Post, Comment, Me, Info, Link, GalleryImage, AdminLoginAttempts

admin.site.register(Post)
admin.site.register(Comment)
admin.site.register(Me)
admin.site.register(Info)
admin.site.register(Link)
admin.site.register(GalleryImage)
admin.site.register(AdminLoginAttempts)

