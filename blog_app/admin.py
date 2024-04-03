from django.contrib import admin
from blog_app.models import Post


class PostModelAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', ]


admin.site.register(Post, PostModelAdmin)