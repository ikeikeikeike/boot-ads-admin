import hashlib

from django.db import models
from django.conf import settings
from django.contrib.auth import models as authmodel

from django_extensions.db.fields import AutoSlugField
from imagekit.models import ImageSpecField
from imagekit.processors import ResizeToFill
from taggit.managers import TaggableManager
from taggit.models import TaggedItemBase
from tinymce.models import HTMLField

from core import basemodel


def _upload_to_image(instance, filename):
    ins = instance
    pre = ins.__class__.__name__.lower()
    path = ins.name or ins.image.url
    return f'{pre}/{path}/{filename}'


class Image(basemodel.BaseModel):
    """
    Image Storages
    """
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, null=False,
        related_name='images', on_delete=models.CASCADE
    )
    groups = models.ManyToManyField(
        authmodel.Group, related_name='images'
    )

    name = models.CharField(max_length=255, null=False)
    mime = models.CharField(max_length=64, null=False, default='')

    image = models.ImageField(
        "Image", null=False, upload_to=_upload_to_image
    )  # blank=True,

    large = ImageSpecField(
        source="image", format='JPEG',
        processors=[ResizeToFill(1280, 1024)],
    )
    middle = ImageSpecField(
        source='image', format="JPEG",
        processors=[ResizeToFill(600, 400)],
        options={'quality': 75}
    )
    thumb = ImageSpecField(
        source='image', format="JPEG",
        processors=[ResizeToFill(250, 250)],
        options={'quality': 60}
    )
    small = ImageSpecField(
        source='image', format="JPEG",
        processors=[ResizeToFill(75, 75)],
        options={'quality': 50}
    )

    class Meta:
        db_table = 'images'


class Category(basemodel.BaseModel):
    name = models.CharField(max_length=255, null=False)
    slug = AutoSlugField(
        null=False, unique=True, editable=True,
        populate_from=['name'],
        help_text='!! must not be edited after publish !!'
    )

    parent = models.ForeignKey(
        'self', blank=True, null=True,
        related_name='children', on_delete=models.CASCADE
    )

    class Meta:
        """
        enforcing that there can not be two
        categories under a parent with same slug
        """
        db_table = 'categories'
        unique_together = ('slug', 'parent', )
        verbose_name_plural = 'categories'

    def __str__(self):
        """
        __str__ method elaborated later in
        post.  use __unicode__ in place of
        __str__ if you are using python 2
        """
        return ' -> '.join(self.paths())

    def paths(self):
        full_path = [self.name]

        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return full_path[::-1]


class PostsTag(TaggedItemBase):
    post_id = models.IntegerField(
        db_index=True, null=False
    )
    content_object = models.ForeignKey(
        'Post', null=False,
        related_name='posts_tags', on_delete=models.CASCADE
    )

    class Meta:
        db_table = 'posts_tags'

    def save(self, *args, **kwargs):
        self.post_id = self.content_object.id
        super().save(*args, **kwargs)


def _upload_to_post(instance, filename):
    ins = instance
    pre = ins.__class__.__name__.lower()
    path = ins.slug or hashlib.md5(ins.title.encode()).hexdigest()
    return f'{pre}/{path}/{filename}'


class Post(basemodel.BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, null=False,
        related_name='posts', on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, null=True, blank=True,
        related_name='posts', on_delete=models.CASCADE
    )

    external_link = models.URLField(
        null=True, blank=True, max_length=255,
        help_text='''
        !! if this value is existance,
        atag link will be set external site !!
        '''
    )
    slug = AutoSlugField(
        unique=True, null=False, editable=True,
        populate_from=['created_at', 'category_slug', 'title'],
        help_text='!! must not be edited after publish !!'
    )

    title = models.CharField(max_length=255, null=False)
    content = HTMLField('Content', null=True, blank=True)

    image = models.ImageField(
        "Image", null=False, upload_to=_upload_to_post
    )  # blank=True,

    publish = models.BooleanField(default=False, null=False)
    publish_at = models.DateField(
        null=True, blank=True,
        auto_now=False, auto_now_add=False
    )

    large = ImageSpecField(
        source="image", format='JPEG',
        processors=[ResizeToFill(1280, 1024)],
    )
    middle = ImageSpecField(
        source='image', format="JPEG",
        processors=[ResizeToFill(600, 400)],
        options={'quality': 75}
    )
    thumb = ImageSpecField(
        source='image', format="JPEG",
        processors=[ResizeToFill(250, 250)],
        options={'quality': 60}
    )
    small = ImageSpecField(
        source='image', format="JPEG",
        processors=[ResizeToFill(75, 75)],
        options={'quality': 50}
    )

    tags = TaggableManager(blank=True, through=PostsTag)

    class Meta:
        db_table = 'posts'

    def category_paths(self):
        """
        for now ignore this instance method,
        """
        k = self.category
        breadcrumb = ["dummy"]
        while k is not None:
            breadcrumb.append(k.slug)
            k = k.parent

        for i in range(len(breadcrumb) - 1):
            breadcrumb[i] = '/'.join(breadcrumb[-1:i - 1:-1])
        return breadcrumb[-1:0:-1]

    def category_slug(self):
        if self.category:
            return self.category.slug
        return ''
