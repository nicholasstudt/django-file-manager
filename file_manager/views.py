import codecs
import mimetypes
import os

from datetime import datetime
from grp import getgrgid
from pwd import getpwuid

from django import http, template
from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response, redirect
from django.utils.translation import ugettext as _

from file_manager import forms
from file_manager import utils

#@staff_member_required
def create(request, url=None):
    # Create a new text file.
    url = utils.clean_path(url)
    parent = '/'.join(url.split('/')[:-1])
    full_path = os.path.join(utils.get_document_root(), url)

    if request.method == 'POST': 
        form = forms.CreateForm(full_path, None, request.POST) 

        if form.is_valid(): 
            file = codecs.open(os.path.join(full_path, form.cleaned_data['name']), encoding='utf-8', mode='w+')

            # FIXME: This shoule check the originals line ending and
            # preserve it.

            # This makes it be \r\n be just \n
            file.write(form.cleaned_data['content'].replace('\r\n', '\n'))
            file.close()

            return redirect('admin_file_manager_list', url=url)
    else:
        # Read the data from file
        form = forms.CreateForm(full_path, None) # An unbound form 

    return render_to_response("admin/file_manager/create.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))
create = staff_member_required(create)

#@staff_member_required
def copy(request, url=None):
    pass
copy = staff_member_required(copy)

#@staff_member_required
def index(request, url=None):
    """
        Show list of files in a url
    """
 
    perms = [ '---', '--x', '-w-', '-wx', 'r--', 'r-x', 'rw-', 'rwx' ]

    url = utils.clean_path(url)

    # Stuff the files in here.
    files = []

    full_path = os.path.join(utils.get_document_root(), url)

    try:
        listing = os.listdir(full_path)
    except OSError:
        raise http.Http404
  
    directory = {}

    directory['url'] = url
    directory['parent'] = '/'.join(url.split('/')[:-1])

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
        item['fileurl'] = os.path.join(url, file)
        item['user'] = getpwuid(itemstat.st_uid)[0]
        item['group'] = getgrgid(itemstat.st_gid)[0]

        # size (in bytes ) for use with |filesizeformat
        item['size'] = itemstat.st_size
        
        # type (direcory/file)
        item['directory'] = os.path.isdir(os.path.join(full_path, file))

        # ctime, mtime
        item['ctime'] = datetime.fromtimestamp(itemstat.st_ctime)
        item['mtime'] = datetime.fromtimestamp(itemstat.st_mtime)

        mime = mimetypes.guess_type(os.path.join(full_path, file),False)[0]
  
        # Assume we can't edit anything except text and unknown.
        if not mime:
            item['can_edit'] = True
        elif 'text' in mime:
            item['can_edit'] = True
        else:
            item['can_edit'] = False

        # permissions (numeric)
        octs = "%04d" % int(oct(itemstat.st_mode & 0777))
        
        dperms = '-'
        if item['directory']:
            item['can_edit'] = False
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

#@staff_member_required
def mkdir(request, url=None):
    """ 
        Make a new directory at the current url.
    """

    url = utils.clean_path(url)
    full_path = os.path.join(utils.get_document_root(), url)

    if request.method == 'POST': 
        form = forms.NameForm(full_path, None, request.POST) 

        if form.is_valid(): 
            #Make the directory
            os.mkdir(os.path.join(full_path, form.cleaned_data['name']))

            return redirect('admin_file_manager_list', url=url)
    else:
        form = forms.NameForm(full_path, None) # An unbound form 

    return render_to_response("admin/file_manager/mkdir.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))
mkdir = staff_member_required(mkdir)

#@staff_member_required
def delete(request, url=None):
    # Delete a file/directory
    
    url = utils.clean_path(url)
    parent = '/'.join(url.split('/')[:-1])
    full_path = os.path.join(utils.get_document_root(), url)
    full_parent = os.path.join(utils.get_document_root(), parent).rstrip('/')

    if request.method == 'POST': 
        
        # If this is a directory, do the walk
        if os.path.isdir(full_path):
            for root, dirs, files in os.walk(full_path, topdown=False):
                for name in files:
                    os.remove(os.path.join(root, name))
                for name in dirs:
                    os.rmdir(os.path.join(root, name))

            os.rmdir(full_path)
        else:
            os.remove(full_path)

        return redirect('admin_file_manager_list', url=parent)

    filelist = []
    errorlist = []

    # If this is a directory, generate the list of files to be removed.
    if os.path.isdir(full_path):
        filelist.append("/%s" % url)
        for root, dirs, files, in os.walk(full_path):
            for name in files: 
                f = os.path.join(root, name).replace(full_parent, '', 1)
                if not os.access(os.path.join(root), os.W_OK):
                    errorlist.append(f)
                filelist.append(f)

            for name in dirs:
                d = os.path.join(root, name).replace(full_parent, '', 1)
                if not os.access(os.path.join(root), os.W_OK):
                    errorlist.append(d)
                filelist.append(d)
    else:
        if not os.access(full_path, os.W_OK):
            errorlist.append("/%s" % url)

        filelist.append("/%s" % url)
    
    return render_to_response("admin/file_manager/delete.html", 
                             # {'url': url, 'files': sorted(filelist),
                              {'url': url, 'files': filelist.sort(),
                             #  'errorlist':sorted(errorlist),
                               'errorlist':errorlist.sort(),
                               'directory': '',},
                              context_instance=template.RequestContext(request))
delete = staff_member_required(delete)

#@staff_member_required
def move(request, url=None):
    """
        Move file/directory to a new location.
    """

    # Not really happy about the l/rstrips.
    url = utils.clean_path(url)

    parent = '/'.join(url.split('/')[:-1])
    full_parent = os.path.join(utils.get_document_root(), parent).rstrip('/')
    full_path = os.path.join(utils.get_document_root(), url)
    directory = url.replace(parent, "", 1).lstrip('/')

    #setttings.TEMPPATH = fullpath

    if request.method == 'POST': 
        form = forms.DirectoryForm(directory, full_path, request.POST) 

        if form.is_valid(): 
    

            new = os.path.join(form.cleaned_data['parent'], directory)

            #Rename the directory
            os.rename(full_path, new)

            return redirect('admin_file_manager_list', url=parent)
    else:
        form = forms.DirectoryForm(directory, full_path, initial={'parent':full_parent}) 

    return render_to_response("admin/file_manager/move.html", 
                              {'form': form, 'url': url,
                               'current': "/%s" % parent,
                               'directory': os.path.isdir(full_path)},
                              context_instance=template.RequestContext(request))
move = staff_member_required(move)

#@staff_member_required
def rename(request, url=None):
    """
        Rename
    """

    # Not really happy about the l/rstrips.
    url = utils.clean_path(url)
    parent = '/'.join(url.split('/')[:-1])
    full_parent = os.path.join(utils.get_document_root(), parent).rstrip('/')
    full_path = os.path.join(utils.get_document_root(), url)

    if request.method == 'POST': 
        form = forms.NameForm(full_parent, full_path, request.POST) 

        if form.is_valid(): 
            new = os.path.join(full_parent, form.cleaned_data['name'])

            # Rename 
            os.rename(full_path, new)

            return redirect('admin_file_manager_list', url=parent)
    else:
        directory = url.replace(parent, "", 1).lstrip('/')
        data = {'name':directory}
        form = forms.NameForm(full_parent, full_path, initial=data)

    return render_to_response("admin/file_manager/rename.html", 
                              {'form': form, 'url': url, 
                               'directory': os.path.isdir(full_path)},
                              context_instance=template.RequestContext(request))
rename = staff_member_required(rename)

#@staff_member_required
def update(request, url=None):
    """
        Update
    """
    url = utils.clean_path(url)
    parent = '/'.join(url.split('/')[:-1])
    full_path = os.path.join(utils.get_document_root(), url)

    if request.method == 'POST': 
        form = forms.ContentForm(request.POST) 

        if form.is_valid(): 
            file = codecs.open(full_path, encoding='utf-8', mode='w+')

            # FIXME: This shoule check the originals line ending and
            # preserve it.

            # This makes it be \r\n be just \n
            file.write(form.cleaned_data['content'].replace('\r\n', '\n'))
            file.close() 
            
            if request.POST.has_key("_continue"):
                msg = _('The %(name)s "%(obj)s" was updated successfully. %(rest)s') % {'name': 'file', 'obj': url, 'rest': _("You may edit it again below.") }

                return render_to_response("admin/file_manager/update.html", 
                              {'form': form, 'url': url, 'messages': [msg]},
                              context_instance=template.RequestContext(request))
            
            return redirect('admin_file_manager_list', url=parent)
    else:
        # Read the data from file
        try:
            content = open(full_path).read()
        except (IOError, OSError):
            raise http.Http404
 
        data = {'content':content}
        form = forms.ContentForm(initial=data) # An unbound form 

    return render_to_response("admin/file_manager/update.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))
update = staff_member_required(update)

#@staff_member_required
def upload(request, url=None):
    """
        Upload a new file.
    """
    url = utils.clean_path(url)
    path = os.path.join(utils.get_document_root(), url)

    if request.method == 'POST': 
        form = forms.UploadForm(path, data=request.POST, files=request.FILES) 

        if form.is_valid(): 
            file_path = os.path.join(path, form.cleaned_data['file'].name)
            destination = open(file_path, 'wb+')
            for chunk in form.cleaned_data['file'].chunks():
                destination.write(chunk) 

            return redirect('admin_file_manager_list', url=url)
    else:
        form = forms.UploadForm(path)

    return render_to_response("admin/file_manager/upload.html", 
                              {'form': form, 'url': url,},
                              context_instance=template.RequestContext(request))
upload = staff_member_required(upload)
