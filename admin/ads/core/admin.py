from django.contrib import admin
from django.utils import html

from imagekit.admin import AdminThumbnail

from . import models


class ImageAdmin(admin.ModelAdmin):
    list_display = (
        'id', 'group_list', 'user', 'name', 'mime', 'admin_image', 'created_at', 'updated_at'
    )
    list_filter = ('user', 'groups', 'created_at', 'updated_at')
    list_display_links = ('id', 'name', )
    search_fields = ('id', 'name', )
    ordering = ['-id']

    admin_image = AdminThumbnail(image_field='small')

    def image_thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url
        return ""
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"

    def group_list(self, obj):
        return u", ".join(o.name for o in obj.groups.all())
    group_list.short_description = "groups"


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
        'id', 'user', 'category', 'tag_list', 'admin_image', 'external_tag',
        'slug_tag', 'title', 'publish', 'publish_at', 'created_at', 'updated_at'
    )
    list_filter = (
        'created_at', 'updated_at', 'publish_at',
        'publish', 'user', 'category'
    )
    fieldsets = (
        (None, {'fields': (
            'image',
            'title',
            'content',
            'user',
            'category',
            'tags',
            'external_link',
            'slug',
            'publish',
            'publish_at',
        )}),
    )

    list_display_links = ('id', 'title', )
    search_fields = ('id', 'title', 'content')
    ordering = ['-id']

    admin_image = AdminThumbnail(image_field='small')

    def get_queryset(self, request):
        return super().get_queryset(request).prefetch_related('tags')

    def tag_list(self, obj):
        return u", ".join(o.name for o in obj.tags.all())
    tag_list.short_description = "tags"

    def external_tag(self, obj):
        if obj.external_link:
            a = '<a href="{0.external_link}" target="_blank">{0.external_link}</a>'.format(obj)
            return html.format_html(a)
        return ""
    external_tag.allow_tags = True
    external_tag.short_description = "show external page"

    def slug_tag(self, obj):
        if obj.slug:
            a = '<a href="/articles/{0.slug}" target="_blank">{0.slug}</a>'.format(obj)
            return html.format_html(a)
        return ""
    slug_tag.allow_tags = True
    slug_tag.short_description = "show article page"

    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

    def image_thumbnail(self, obj):
        if obj.image:
            return '<img src="%s" />' % obj.image.url
        return ""
    image_thumbnail.allow_tags = True
    image_thumbnail.short_description = "Thumbnail"


admin.site.register(models.Post, PostAdmin)
admin.site.register(models.Image, ImageAdmin)
admin.site.register(models.Category, CategoryAdmin)
