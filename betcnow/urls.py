from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^$', TemplateView.as_view(template_name="betcnow/home.html"), name='home'),
    url(r'^play/$', views.play, name='play'),
    url(r'^gourl_callback.html/$', views.callback, name='callback'),
    url(r'^payment/$', views.payment, name='payment'),
]