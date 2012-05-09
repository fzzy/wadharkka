from django.conf.urls.defaults import patterns, include, url
from django.contrib import admin

admin.autodiscover()

urlpatterns = patterns('',
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    url(r'^admin/', include(admin.site.urls)),
    url(r'', include('social_auth.urls')),
)

urlpatterns += patterns('wadharkka.views',
    url(r'^$', 'home', name='home'),
    url(r'^done/$', 'done', name='done'),
    url(r'^error/$', 'error', name='error'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^form/$', 'form', name='form'),
    url(r'^editor/$', 'editor', name='editor'),
    #r'^wadharkka/', include('wadharkka.foo.urls')),
)

