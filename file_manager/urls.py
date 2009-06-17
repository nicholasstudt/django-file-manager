from django.conf.urls.defaults import *

urlpatterns = patterns('',


    # Directory and File operations
    url(r'^/delete/(?P<url>.*)$', 'file_manager.views.delete', name='delete'),
    url(r'^/copy/(?P<url>.*)$', 'file_manager.views.copy', name='copy'),
    url(r'^/move/(?P<url>.*)$', 'file_manager.views.move', name='move'),
    url(r'^/rename/(?P<url>.*)$', 'file_manager.views.rename', name='rename'),
  
    # File Operations
    url(r'^/create/(?P<url>.*)$', 'file_manager.views.create', name='create'),
    url(r'^/update/(?P<url>.*)$', 'file_manager.views.update', name='update'),
    url(r'^/upload/(?P<url>.*)$', 'file_manager.views.upload', name='upload'),

    # Directory Options.
    url(r'^/mkdir/(?P<url>.*)$', 'file_manager.views.mkdir', name='mkdir'),
    url(r'^/list/(?P<url>.*)$', 'file_manager.views.index', name='list'),
    url(r'^/$', 'file_manager.views.index', name='index'),
)
