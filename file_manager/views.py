from django import http, template
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response

@staff_member_required
def create(request, url=None):
    pass

@staff_member_required
def copy(request, url=None):
    pass

@staff_member_required
def file_index(request, url=None):
    """
    Show list of files in a directory
    """

    # Stuff the files in here.
    files = []

    # 

    return render_to_response("admin/file_manager/index.html", 
                              {
                                'directory': url,
                                'listing': files,
                               },
                              context_instance=template.RequestContext(request))

@staff_member_required
def mkdir(request, url=None):
    pass

@staff_member_required
def delete(request, url=None):
    pass

@staff_member_required
def rename(request, url=None):
    pass

@staff_member_required
def update(request, url=None):
    pass

@staff_member_required
def upload(request, url=None):
    return render_to_response("admin/file_manager/upload.html", 
                              {'data': request.path,
                               'url': url,},
                              context_instance=template.RequestContext(request))



