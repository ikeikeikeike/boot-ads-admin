from django.conf.urls import url

from . import views

urlpatterns = [
    url(r"^imageform$", views.imageform, name="imageform"),
    url(r"^uploadimage$", views.uploadimage, name="uploadimage"),
]
