from django.conf.urls.defaults import *

urlpatterns = patterns('',

    # Directory and File operations
    url(r'^/copy/(?P<url>.*)$', 'file_manager.views.copy', 
        name='admin_file_manager_copy'),

    url(r'^/delete/(?P<url>.*)$', 'file_manager.views.delete',
        name='admin_file_manager_delete'),

    url(r'^/detail/(?P<url>.*)$', 'file_manager.views.detail',
        name='admin_file_manager_detail'),

    url(r'^/move/(?P<url>.*)$', 'file_manager.views.move', 
        name='admin_file_manager_move'),

    url(r'^/permission/(?P<url>.*)$', 'file_manager.views.permission',
        name='admin_file_manager_permission'),

    url(r'^/rename/(?P<url>.*)$', 'file_manager.views.rename', 
        name='admin_file_manager_rename'),

    # Directory Operations
    url(r'^/list/(?P<url>.*)$', 'file_manager.views.index', 
        name='admin_file_manager_list'),

    url(r'^/mkdir/(?P<url>.*)$', 'file_manager.views.mkdir', 
        name='admin_file_manager_mkdir'),

    # File Operations
    url(r'^/create/(?P<url>.*)$', 'file_manager.views.create', 
        name='admin_file_manager_create'),

    url(r'^/update/(?P<url>.*)$', 'file_manager.views.update', 
        name='admin_file_manager_update'),

    url(r'^/upload/(?P<url>.*)$', 'file_manager.views.upload', 
        name='admin_file_manager_upload'),

    url(r'^/upload/$', 'file_manager.views.upload', 
        name='admin_file_manager_upload2'),

    # Link Operations
    url(r'^/mkln/(?P<url>.*)$', 'file_manager.views.mkln', 
        name='admin_file_manager_mkln'),

    # Admin link
    url(r'^/file/(?P<id>.*)/$', 'file_manager.views.admin_redirect', 
        name='admin_file_manager_admin_redirect'),

    # File Listing
    url(r'^/$', 'file_manager.views.index', 
        name='admin_file_manager_index'),
)
