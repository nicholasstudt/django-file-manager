import os 

from django.conf import settings
from django import forms
from django.core import exceptions

class DirectoryPathField(forms.ChoiceField):
    """ 
        Copied directly from FilePathField, alter to show only directories
        only, rather than files.

        showroot=True -- Adds root directory to the options.
    """
    def __init__(self, path, showroot=False, match=None, 
                 recursive=False, required=True, widget=None, label=None, 
                 initial=None, help_text=None, *args, **kwargs):
        self.path, self.match, self.recursive = path, match, recursive
        super(DirectoryPathField, self).__init__(choices=(), required=required,
            widget=widget, label=label, initial=initial, help_text=help_text,
            *args, **kwargs)
        self.choices = []

        # Make "/" valid"
        if showroot:
            d = self.path
            d_short = d.replace(path, "", 1)
            if not d_short:
                d_short = '/'
            self.choices.append((d, d_short))

        if self.match is not None:
            self.match_re = re.compile(self.match)
        if recursive:
            for root, dirs, files in os.walk(self.path):
                for d in dirs:
                    if self.match is None or self.match_re.search(f):
                        d = os.path.join(root, d)
                        d_short = d.replace(path, "", 1)
                        self.choices.append((d, d_short))
        else:
            try:
                for f in os.listdir(self.path):
                    full_file = os.path.join(self.path, f)
                    if os.path.isdir(full_file) and (self.match is None or self.match_re.search(f)):
                        self.choices.append((full_file, full_file.replace(path, "", 1)))
            except OSError:
                pass
        self.widget.choices = self.choices

class DirectoryForm(forms.Form):

    if not settings.DOCUMENT_ROOT:
        raise exceptions.ImproperlyConfigured, "DOCUMENT_ROOT variable not defined in settings.py"

    document_root = settings.DOCUMENT_ROOT

    parent = DirectoryPathField(path=document_root,recursive=True,showroot=True)

    def clean_parent(self):
        parent = self.cleaned_data['parent']
       
        if not os.access(parent, os.W_OK):
            raise forms.ValidationError("Can not write to directory.")

        return parent

class NameForm(forms.Form):
    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data['name']
       
        if os.access(name, os.F_OK):
            raise forms.ValidationError("Name already exists.")

        return name 

class ContentForm(forms.Form):
    content = forms.CharField()

class FileForm(forms.Form):

    if not settings.DOCUMENT_ROOT:
        raise exceptions.ImproperlyConfigured, "DOCUMENT_ROOT variable not defined in settings.py"

    document_root = settings.DOCUMENT_ROOT

    parent = DirectoryPathField(path=document_root,recursive=True)
    name = forms.CharField()
    content = forms.CharField()

class UploadForm(forms.Form):

    if not settings.DOCUMENT_ROOT:
        raise exceptions.ImproperlyConfigured, "DOCUMENT_ROOT variable not defined in settings.py"

    document_root = settings.DOCUMENT_ROOT

    parent = DirectoryPathField(path=document_root,recursive=True)
    name = forms.CharField()
    content = forms.CharField()
