import os
from datetime import datetime
from grp import getgrgid
from pwd import getpwuid

from django import http, template
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, redirect

from file_manager import forms
from file_manager import utils

@staff_member_required
def create(request, url=None):
    pass

@staff_member_required
def copy(request, url=None):
    pass

def index(request, url=None):
    """
    Show list of files in a directory
    """
 
    perms = [ '---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx' ]

    clean_url = utils.clean_path(url)

    # Stuff the files in here.
    files = []

    full_path = os.path.join(utils.get_document_root(), clean_url)

    listing = os.listdir(full_path)
  
    directory = {}

    directory['url'] = clean_url
    directory['parent'] = '/'.join(clean_url.split('/')[:-1])

    if os.access(full_path, os.R_OK):
        directory['can_read'] = True
    else:
        directory['can_read'] = False 
    
    if os.access(full_path, os.W_OK):
        directory['can_write'] = True
    else:
        directory['can_write'] = False

    for file in listing:
        itemstat = os.stat(os.path.join(full_path, file))

        item = {}
        item['filename'] = file
        item['fileurl'] = os.path.join(clean_url, file)
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
     
        if os.access(os.path.join(full_path, file), os.R_OK):
            item['can_read'] = True
        else:
            item['can_read'] = False

        if os.access(os.path.join(full_path, file), os.W_OK):
            item['can_write'] = True
        else:
            item['can_write'] = False

        files.append(item)
    
    return render_to_response("admin/file_manager/index.html", 
                              {'directory': directory,
                               'files': files,},
                              context_instance=template.RequestContext(request))
index = staff_member_required(index)

@staff_member_required
def mkdir(request, url=None):

    # Not really happy about the l/rstrips.
    clean_url = utils.clean_path(url)
    parent = '/'.join(clean_url.split('/')[:-1])
    full_path = os.path.join(utils.get_document_root(), clean_url)

    if request.method == 'POST': 
        form = forms.DirectoryForm(request.POST) 

        if form.is_valid(): 
            new = os.path.join(form.cleaned_data['parent'], 
                               form.cleaned_data['name'])

            #Make the directory
            os.mkdir(new)

            return redirect('list', url=clean_url)
    else:
        data = {'parent':full_path}
        form = forms.DirectoryForm(initial=data) # An unbound form 

    return render_to_response("admin/file_manager/mkdir.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))

@staff_member_required
def delete(request, url=None):
    pass

@staff_member_required
def rename(request, url=None):

    # Not really happy about the l/rstrips.
    clean_url = utils.clean_path(url)
    parent = '/'.join(clean_url.split('/')[:-1])
    full_path = os.path.join(utils.get_document_root(), clean_url)
    full_parent = os.path.join(utils.get_document_root(), parent).rstrip('/')
    directory = clean_url.replace(parent, "", 1).lstrip('/')

    if request.method == 'POST': 
        form = forms.DirectoryForm(request.POST) 

        if form.is_valid(): 
            new = os.path.join(form.cleaned_data['parent'], 
                               form.cleaned_data['name'])

            #Rename the directory
            os.rename(full_path, new)

            return redirect('list', url=parent)
    else:
        data = {'parent':full_parent, 'name':directory}
        form = forms.DirectoryForm(initial=data) # An unbound form 

    return render_to_response("admin/file_manager/rename.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))

@staff_member_required
def update(request, url=None):
    clean_url = utils.clean_path(url)
    parent = '/'.join(clean_url.split('/')[:-1])
    full_path = os.path.join(utils.get_document_root(), clean_url)

    if request.method == 'POST': 
        form = forms.DirectoryForm(request.POST) 

        if form.is_valid(): 
            #Rename the directory

            return redirect('list', url=parent)
    else:
        data = {}
        form = forms.DirectoryForm(initial=data) # An unbound form 

    return render_to_response("admin/file_manager/update.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))

@staff_member_required
def upload(request, url=None):
    return render_to_response("admin/file_manager/upload.html", 
                              {'data': request.path,
                               'url': url,},
                              context_instance=template.RequestContext(request))



