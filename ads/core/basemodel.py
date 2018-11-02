from __future__ import unicode_literals

from datetime import datetime as dt

from django.db import models
from django.utils import timezone


def asstr(dct):
    r = {}
    for k, v in dct.items():
        if k not in ['_state', 'content', 'created_at', 'updated_at']:
            if isinstance(v, dt):
                r.update({k: str(v)})
            else:
                r.update({k: v})
    return str(r)


class BaseModel(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=False)

    updated_at = models.DateTimeField(
        auto_now=True,
        editable=False,
        db_index=False)

    def __str__(self):
        return asstr(self.__dict__)

    class Meta:
        ordering = ["-id"]
        abstract = True


class SimplyModel(models.Model):
    created_at = models.DateTimeField(
        default=timezone.now,
        editable=False,
        db_index=False)

    def __str__(self):
        return asstr(self.__dict__)

    class Meta:
        ordering = ["-id"]
        abstract = True
