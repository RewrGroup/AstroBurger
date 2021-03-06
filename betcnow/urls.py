from django.conf.urls import url
from . import views
from django.views.generic import TemplateView

urlpatterns = [
    url(r'^terms-of-use/$', TemplateView.as_view(template_name='betcnow/terminos.html'), name="terminos"),
    url(r'^privacy-policy/$', TemplateView.as_view(template_name='betcnow/privacidad.html'), name="privacidad"),
    url(r'^$', TemplateView.as_view(template_name="betcnow/home.html"), name='home'),
    url(r'^profile_redirect/$', views.profile_redirect, name="profile_redirect"),
    url(r'^play/$', views.play, name='play'),
    url(r'^demo/$', views.demo, name='demo'),
    url(r'^gourl_callback.html/$', views.callback, name='callback'),
    url(r'^gourl_callback_memberships/$', views.membership_callback, name='membership_callback'),
    url(r'^check-out/$', views.checkout, name='check-out'),
    url(r'^has-paid/$', views.has_paid, name='has_paid'),
    url(r'^reg-demo/$', views.registrar_demo, name='reg-demo'),
    url(r'^user/(?P<pk>[0-9]+)/$', views.profile, name='profile'),
    url(r'^memberships/$', views.upgrade, name='membership'),
    url(r'^about/$', TemplateView.as_view(template_name="betcnow/about.html"), name='about'),
    url(r'^testimonials/$', views.testimonios, name='testimonios'),
    url(r'^proccess_testimonial', views.proccess_testimonial, name='proccess_testimonial'),
    url(r'^results/$', views.results, name='results'),
    url(r'^results/betcpot/(?P<pk>[0-9]+)/$', views.resultado_pote, name='betcpot_result'),
    url(r'^redeem/$', views.redeem, name='redeem'),
    url(r'^notification-read/$', views.notification_read, name='notification_read'),
]