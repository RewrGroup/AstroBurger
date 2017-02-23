from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="betcnow/home.html"), name='home'),
    url(r'^play/$', views.play, name='play'),
    url(r'^gourl_callback.html/$', views.callback, name='callback'),
    url(r'^check-out/$', views.checkout, name='check-out'),
    url(r'^has_paid/$', views.has_paid, name='has_paid'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^membership/$', TemplateView.as_view(template_name="betcnow/upgrade.html"), name='membership'),
    url(r'^about/$', TemplateView.as_view(template_name="betcnow/about.html"), name='about'),
]