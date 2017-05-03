from django.conf.urls import url
from . import apis


urlpatterns = [
    url(r'^save_hotels$', apis.save_hotels, name='save_hotels'),
    url(r'^save_comments$', apis.save_comments, name='save_comments'),
    url(r'^get_comments$', apis.get_comments, name='get_comments')
]
