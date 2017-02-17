from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="betcnow/home.html"), name='home'),
    url(r'^play/$', views.play, name='play'),
    url(r'^gourl_callback.html/$', views.callback, name='callback'),
    url(r'^check-out/$', views.checkout, name='check-out'),
    url(r'^jugada_timeout/$', views.jugada_timeout, name='timeout'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.profile, name='profile')
]