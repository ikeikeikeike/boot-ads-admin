from django.db import models
from django.conf import settings

from tinymce.models import HTMLField

from core import basemodel


class Category(basemodel.BaseModel):
    name = models.CharField(max_length=255, null=False)
    slug = models.SlugField(null=False)
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
        full_path = [self.name]

        k = self.parent
        while k is not None:
            full_path.append(k.name)
            k = k.parent

        return ' -> '.join(full_path[::-1])


class Post(basemodel.BaseModel):
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, default=1, null=False,
        related_name='posts', on_delete=models.CASCADE
    )
    category = models.ForeignKey(
        Category, null=True, blank=True,
        related_name='posts', on_delete=models.CASCADE
    )

    title = models.CharField(max_length=255, null=False)
    content = HTMLField('Content', null=False)

    slug = models.SlugField(unique=True, null=False)
    draft = models.BooleanField(default=False, null=False)

    publish = models.DateField(
        null=True, blank=True,
        auto_now=False, auto_now_add=False
    )

    class Meta:
        db_table = 'posts'

    def get_cat_list(self):
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
