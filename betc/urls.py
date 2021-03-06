"""jupiter URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from django.conf.urls import url, include
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from betcnow.regbackend import MyRegistrationView, RefRegistrationView
from betcnow.forms import LoginWithPlaceholder
from betcnow.views import remember_me_login
from betcnow.views import SendEmailAfterActivate
from django.views.generic.base import TemplateView
from django.contrib.sitemaps.views import sitemap
from betcnow.sitemaps import ViewSitemap

sitemaps = {'views': ViewSitemap}

urlpatterns = [
    url(r'', include('betcnow.urls')),
    url(r'^robots.txt/$', TemplateView.as_view(template_name='robots.txt', content_type='text/plain'), name="robots"),
    url(r'^accounts/register/$',
        MyRegistrationView.as_view(),
        name='registration_register'),
    url(r'^ref=(?P<pk>[0-9]+)/$',
        RefRegistrationView.as_view(),
        name='ref_register'),
    url(r'^accounts/login/$', remember_me_login, {'template_name': 'registration/login.html',
                                                  'authentication_form': LoginWithPlaceholder},
        name='login'),
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        SendEmailAfterActivate.as_view(),
        name='registration_activate'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', admin.site.urls),
    url(r'^notifications/', include('pinax.notifications.urls')),
    url(r'^sitemap\.xml$', sitemap, {'sitemaps': sitemaps}, name='django.contrib.sitemaps.views.sitemap')
]
"""

# Estas son las URLs para el "estamos trabajando"
urlpatterns = [
    url(r'^terms_of_use/$', TemplateView.as_view(template_name='betcnow/terminos.html'), name="terminos"),
    url(r'^privacy_policy/$', TemplateView.as_view(template_name='betcnow/privacidad.html'), name="privacidad"),
    url(r'^$',
        TemplateView.as_view(template_name='betcnow/working.html'),
        name='home'),
    url(r'^admin/', admin.site.urls),
]
"""
if settings.DEBUG:
    import debug_toolbar

    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)), ]
