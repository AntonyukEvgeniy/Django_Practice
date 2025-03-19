from django.contrib import admin
from .models import BlogPost
@admin.register(BlogPost)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = ('title', 'created_at', 'published', 'views_count')
    list_filter = ('published',)
    search_fields = ('title', 'content')