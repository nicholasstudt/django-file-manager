from django.contrib import admin
from django.conf.urls.defaults import *
from django.utils.functional import lazy
from django.core.urlresolvers import reverse

from file_manager.models import File 

reverse_lazy = lazy(reverse, unicode)

class FileAdmin(admin.ModelAdmin):
    """
    This is only to get the File Manager to register itself into the
    admin.
    """
    def get_urls(self):
        urls = patterns('django.views.generic.simple',
                        url(r'^$', 'redirect_to', 
                            {'url': reverse_lazy('admin_file_manager_index')},
                            name="file_manager_applicationdefinition_changelist"),
                        
                        url(r'^add/$', 'redirect_to', 
                            {'url': reverse_lazy('admin_file_manager_upload2')},
                            name="file_manager_applicationdefinition_add"),
                        )
        return urls
admin.site.register(File, FileAdmin)
