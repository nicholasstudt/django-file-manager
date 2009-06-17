import os 

from django.conf import settings
from django import forms
from django.core import exceptions
from django.utils.translation import ugettext as _

from file_manager import utils

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
        self.widget.choices = sorted(self.choices)

class DirectoryForm(forms.Form):

    def __init__(self, file, original, *args, **kwargs):
        self.file = file 
        self.original = original 
        super(DirectoryForm, self).__init__(*args, **kwargs)

    document_root = utils.get_document_root()

    parent = DirectoryPathField(path=document_root,recursive=True,showroot=True)

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        path = os.path.join(parent, self.file)
        
        if self.original != path: # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Destination already exists.'))

        if not os.access(parent, os.W_OK):
            raise forms.ValidationError(_('Can not write to directory.'))

        return parent

class NameForm(forms.Form):

    def __init__(self, path, original, *args, **kwargs):
        self.path = path
        self.original = original
        super(NameForm, self).__init__(*args, **kwargs)

    name = forms.CharField()

    def clean_name(self):
        name = self.cleaned_data['name']
        
        path = os.path.join(self.path, name)

        if self.original != path: # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Name already exists.'))

        return name 

class ContentForm(forms.Form):
    content = forms.CharField(widget=forms.widgets.Textarea())

class CreateForm(NameForm,ContentForm):
    pass

class UploadForm(forms.Form):

    def __init__(self, path, *args, **kwargs):
        self.path = path
        super(UploadForm, self).__init__(*args, **kwargs)

    file = forms.FileField()

    def clean_file(self):
        filename = self.cleaned_data['file'].name 

        if os.access(os.path.join(self.path, filename), os.F_OK):
            raise forms.ValidationError(_('File already exists.')) 
        
        # CHECK FILESIZE
        filesize = self.cleaned_data['file'].size
        if filesize > utils.get_max_upload_size():
            raise forms.ValidationError(_(u'Filesize exceeds allowed Upload Size.'))

        return self.cleaned_data['file']
