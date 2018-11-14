from django import http
from django import shortcuts
from django.db.models import Q
from django.contrib.auth import decorators

from core import models


@decorators.login_required
def imageform(request):
    where = Q(groups__in=request.user.groups.all()) | Q(user=request.user)

    return shortcuts.render(request, 'post/imageform.html', {
        'images': models.Image.objects.filter(where)
    })


@decorators.login_required
def uploadimage(request):
    paths, u = [], request.user
    for _, i in request.FILES.items():
        kargs = dict(name=i.name, mime=i.content_type, image=i, user=u)

        img = models.Image.objects.create(**kargs)
        for group in u.groups.all():
            img.groups.add(group)

        paths.append(img.image.url)

    return http.JsonResponse({'paths': paths})
