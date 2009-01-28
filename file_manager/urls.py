from django.conf.urls.defaults import *

urlpatterns = patterns('',

    # /mkdir/(path)
    # /rename/(path)
    # /delete/(path)
    # /upload/(path)
    # /copy/(path/file)
    # /edit/(path/file)
    # /create/(path)
    # /(path) show index

    # (?P<dir_name>[_a-zA-Z0-9./-]+)

    url(r'^mkdir/(?P<url>.*)$', 'file_manager.views.mkdir', name='mkdir'),

    url(r'^rename/(?P<url>.*)$', 'file_manager.views.rename', name='rename'),

    url(r'^delete/(?P<url>.*)$', 'file_manager.views.delete', name='delete'),

    url(r'^upload/(?P<url>.*)$', 'file_manager.views.upload', name='upload'),

    url(r'^copy/(?P<url>.*)$', 'file_manager.views.copy', name='copy'),

    # For file
    url(r'^edit/(?P<url>.*)$', 'file_manager.views.update', name='update'),

    # For file
    url(r'^create/(?P<url>.*)$', 'file_manager.views.create', name='create'),

    url(r'^/(?P<url>.*)$', 'file_manager.views.index', name='index'),

    # Is this redundant ?
    #url(r'^$', 'file_manager.views.index', name='main-index'),

)
