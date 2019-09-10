"""cert_manage URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.conf import settings
from django.conf.urls import url, include
from django.conf.urls.static import static
from cert_manage.views import IndexView

urlpatterns = [
    url(r'^$', IndexView.as_view(), name='index'),
    url(r'^users/', include('users.urls.views_urls', namespace='users')),
    url(r'^certs/', include('certs.urls.views_urls', namespace='certs')),

    url(r'^api/users/', include('users.urls.api_urls', namespace='api-users')),
    url(r'^api/certs/', include('certs.urls.api_urls', namespace='api-certs')),
    # External apps url
    url(r'^admin/', admin.site.urls),
    url(r'^captcha/', include('captcha.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) \
               + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
