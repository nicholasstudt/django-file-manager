from django.conf.urls.defaults import *

urlpatterns = patterns('',

    # Directory and File operations
    url(r'^/delete/(?P<url>.*)$', 'file_manager.views.delete',
        name='admin_file_manager_delete'),

    url(r'^/copy/(?P<url>.*)$', 'file_manager.views.copy', 
        name='admin_file_manager_copy'),

    url(r'^/move/(?P<url>.*)$', 'file_manager.views.move', 
        name='admin_file_manager_move'),

    url(r'^/rename/(?P<url>.*)$', 'file_manager.views.rename', 
        name='admin_file_manager_rename'),
  
    # File Operations
    url(r'^/create/(?P<url>.*)$', 'file_manager.views.create', 
        name='admin_file_manager_create'),

    url(r'^/update/(?P<url>.*)$', 'file_manager.views.update', 
        name='admin_file_manager_update'),

    url(r'^/upload/(?P<url>.*)$', 'file_manager.views.upload', 
        name='admin_file_manager_upload'),

    # Directory Options.
    url(r'^/mkdir/(?P<url>.*)$', 'file_manager.views.mkdir', 
        name='admin_file_manager_mkdir'),

    url(r'^/list/(?P<url>.*)$', 'file_manager.views.index', 
        name='admin_file_manager_list'),

    url(r'^/$', 'file_manager.views.index', 
        name='admin_file_manager_index'),
)
