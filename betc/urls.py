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

"""
urlpatterns = [
    url(r'', include('betcnow.urls')),
    url(r'^accounts/register/$',
        MyRegistrationView.as_view(),
        name='registration_register'),
    url(r'^accounts/register/ref=(?P<pk>[0-9]+)/$',
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
]
"""

# Estas son las URLs para el countdown
urlpatterns = [
    url(r'^$',
        MyRegistrationView.as_view(),
        name='countdown_register'),
    url(r'^ref=(?P<pk>[0-9]+)/$',
        RefRegistrationView.as_view(),
        name='countdown_ref_register'),
    url(r'^accounts/activate/complete/$',
        TemplateView.as_view(template_name='registration/activation_complete.html'),
        name='registration_activation_complete'),
    url(r'^accounts/activate/(?P<activation_key>\w+)/$',
        SendEmailAfterActivate.as_view(),
        name='registration_activate'),
    url(r'^accounts/', include('registration.backends.default.urls')),
    url(r'^admin/', admin.site.urls),
]

if settings.DEBUG:
    import debug_toolbar
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += staticfiles_urlpatterns()
    urlpatterns += [url(r'^__debug__/', include(debug_toolbar.urls)), ]