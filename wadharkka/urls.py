from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('wadharkka.views',
    url(r'^$', 'editor', name='editor'),
    # url(r'^wadharkka/', include('wadharkka.foo.urls')),
)

