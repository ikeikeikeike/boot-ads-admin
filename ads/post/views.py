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
    for _, img in request.FILES.items():
        kargs = dict(name=img.name, image=img, user=u)

        image = models.Image.objects.create(**kargs)
        for group in u.groups.all():
            image.groups.add(group)

        paths.append(image.image.url)

    return http.JsonResponse({'paths': paths})
