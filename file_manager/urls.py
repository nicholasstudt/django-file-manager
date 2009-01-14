from django.conf.urls.defaults import *

urlpatterns = patterns('',

    # /directories
    #   /mkdir/(path)
    #   /rename/(path)
    #   /copy/(path)
    #   /delete/(path)
    #   /(path) show index
    # /files
    #   /add/(path)
    #   /edit/(path/file)
    #   /copy/(path/file)
    #   /delete/(path/file)
    #   /upload/(path)

    # (?P<dir_name>[_a-zA-Z0-9./-]+)

    url(r'^file/add/(?P<url>.*)/$', 'file_manager.views.add_file', name="file_add"),


)
