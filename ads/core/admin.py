from django.contrib import admin

from . import models


class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        'id', '__str__', 'name', 'slug', 'parent',
        'created_at', 'updated_at'
    )
    list_filter = ('created_at', 'updated_at', 'parent')
    list_display_links = ('id', '__str__', )
    search_fields = ('id', 'name', )
    ordering = ['-id']


class PostAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'user', 'category', 'title', 'slug', 'draft', 'publish',
        'created_at', 'updated_at'
    )
    list_filter = (
        'created_at', 'updated_at',
        'draft', 'user', 'category'
    )
    list_display_links = ('id', 'title', )
    search_fields = ('id', 'title', 'content')
    ordering = ['-id']


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Category, CategoryAdmin)
