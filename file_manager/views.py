import os
import urllib

from datetime import datetime
from grp import getgrgid
from pwd import getpwuid

from django import http, template
from django.core.exceptions import ImproperlyConfigured
from django.conf import settings
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response

def _get_document_root():
    if not settings.DOCUMENT_ROOT:
        raise ImproperlyConfigured, 'file_manager requires DOCUMENT_ROOT variable be defined in settings.py' 

    return settings.DOCUMENT_ROOT

def _clean_path(url):
    """
    Makes the path safe from ..
    """
    if not url:
        return '' 

    result = ''
    path = os.path.normpath(urllib.unquote(url))
    path = path.lstrip('/')
    for part in path.split('/'):
        if not part:
            # Strip empty path components.
            continue
        drive, part = os.path.splitdrive(part)
        head, part = os.path.split(part)
        if part in (os.curdir, os.pardir):
            # Strip '.' and '..' in path.
            continue
        result = os.path.join(result, part).replace('\\', '/')
        
    if result and path != result or not path:
        result = ''
    
    return result
    

@staff_member_required
def create(request, url=None):
    pass

@staff_member_required
def copy(request, url=None):
    pass

def file_index(request, url=None):
    """
    Show list of files in a directory
    """
  
    perms = [ '---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx' ]

    clean_url = _clean_path(url)

    # Stuff the files in here.
    files = []
    directories = []

    full_path = os.path.join(_get_document_root(), clean_url)

    listing = os.listdir(full_path)

    for file in listing:
        itemstat = os.stat(os.path.join(full_path, file))

        item = {}
        item['filename'] = file
        item['user'] = getpwuid(itemstat.st_uid)[0]
        item['group'] = getgrgid(itemstat.st_gid)[0]

        # size (in bytes ) for use with |filesizeformat
        item['size'] = itemstat.st_size
        
        # type (direcory/file)
        item['directory'] = os.path.isdir(os.path.join(full_path, file))

        # ctime, mtime
        item['ctime'] = datetime.fromtimestamp(itemstat.st_ctime)
        item['mtime'] = datetime.fromtimestamp(itemstat.st_mtime)

        # permissions (numeric)
        octs = "%04d" % int(oct(itemstat.st_mode & 0777))
        
        dperms = '-'
        if item['directory']:
            dperms = 'd'

        item['perms_numeric'] = octs
        item['perms'] = "%s%s%s%s" % (dperms, perms[int(octs[1])], 
                                      perms[int(octs[2])], perms[int(octs[3])])
       
        if item['directory']:
            directories.append(item)
        else:
            files.append(item)
    
    return render_to_response("admin/file_manager/index.html", 
                              {'directory': clean_url,
                               'files': files,
                               'directories': directories,},
                              context_instance=template.RequestContext(request))
file_index = staff_member_required(file_index)

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



