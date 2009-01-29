from django.conf.urls.defaults import *

urlpatterns = patterns('',
    
    url(r'^/create/(?P<url>.*)$', 'file_manager.views.create', name='create'),
    url(r'^/copy/(?P<url>.*)$', 'file_manager.views.copy', name='copy'),
    url(r'^/delete/(?P<url>.*)$', 'file_manager.views.delete', name='delete'),
    url(r'^/mkdir/(?P<url>.*)$', 'file_manager.views.mkdir', name='mkdir'),
    url(r'^/rename/(?P<url>.*)$', 'file_manager.views.rename', name='rename'),
    url(r'^/update/(?P<url>.*)$', 'file_manager.views.update', name='update'),
    url(r'^/upload/(?P<url>.*)$', 'file_manager.views.upload', name='upload'),

    # Need to have a "root" for viewing, so we don't get clash with
    # actions above. 
    url(r'^/v(?P<url>.*)$', 'file_manager.views.file_index', name='index'),
    url(r'^/$', 'file_manager.views.file_index', name='fileindex'),
)
