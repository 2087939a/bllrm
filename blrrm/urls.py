from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf import settings
urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'blrrm.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^app/', include('app.urls')),
)


if not settings.DEBUG:
        urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)