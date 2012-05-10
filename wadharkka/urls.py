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
    url(r'^document/create/', 'create_document', name='create_document'),
    url(r'^document/edit/(?P<id>\d+)/', 'edit_document', name='edit_document'),
    url(r'^document/show/(?P<id>\d+)/', 'show_document', name='show_document'),
    url(r'^document/share/(?P<id>\d+)/', 'share_document', name='share_document'),
    url(r'^preview_parser/', 'preview_parser', name='preview_parser'),
)

