import os 

from django import forms
from django.utils.translation import ugettext as _

from file_manager import utils

class DirectoryFileForm(forms.Form):

    link = forms.ChoiceField(help_text=_('Link Destination'))

    def __init__(self, file, *args, **kwargs):
        self.file = file 
        self.document_root = utils.get_document_root()
        super(DirectoryFileForm, self).__init__(*args, **kwargs)
    
        # Set the choices dynamicly.
        self.fields['link'].choices = self.make_choices()

    def make_choices(self):
 
        choices = []

        # Make "/" valid"
        d = self.document_root
        d_short = d.replace(self.document_root, "", 1)
        if not d_short:
            d_short = '/'
        
        choices.append((d, d_short))

        for root, dirs, files in os.walk(self.document_root):
            for d in dirs:
                d = os.path.join(root, d)
                d_short = d.replace(self.document_root, "", 1)
                choices.append((d, d_short))
            for f in files:
                f = os.path.join(root, f)
                f_short = f.replace(self.document_root, "", 1)
                choices.append((f, f_short))


        #return sorted(choices)      
        choices.sort()
        return choices

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        path = os.path.join(parent, self.file)

        if self.original != path: # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Destination already exists.'))
            if path.startswith(self.original):
                raise forms.ValidationError(_('Can\'t move directory into itself.'))

        if not os.access(parent, os.W_OK):
            raise forms.ValidationError(_('Can not write to directory.'))

        return parent



class DirectoryForm(forms.Form):

    parent = forms.ChoiceField(help_text=_('Destination Directory'))

    def __init__(self, file, original, *args, **kwargs):
        self.file = file 
        self.original = original 
        self.document_root = utils.get_document_root()
        super(DirectoryForm, self).__init__(*args, **kwargs)
    
        # Set the choices dynamicly.
        self.fields['parent'].choices = self.make_choices()

    def make_choices(self):
 
        choices = []

        # Make "/" valid"
        d = self.document_root
        d_short = d.replace(self.document_root, "", 1)
        if not d_short:
            d_short = '/'
        
        choices.append((d, d_short))

        for root, dirs, files in os.walk(self.document_root):
            for d in dirs:
                d = os.path.join(root, d)
                if not d.startswith(self.original): 
                    d_short = d.replace(self.document_root, "", 1)
                    choices.append((d, d_short))

        #return sorted(choices)      
        choices.sort()
        return choices

    def clean_parent(self):
        parent = self.cleaned_data['parent']

        path = os.path.join(parent, self.file)

        if self.original != path: # Let no change work correctly.
            if os.access(path, os.F_OK):
                raise forms.ValidationError(_('Destination already exists.'))
            if path.startswith(self.original):
                raise forms.ValidationError(_('Can\'t move directory into itself.'))

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
    attrs = { 'class': 'vLargeTextField' }
    content = forms.CharField(widget=forms.widgets.Textarea(attrs=attrs))

class CreateForm(NameForm,ContentForm):
    pass

class CopyForm(NameForm,DirectoryForm):

    def clean(self):
        cleaned_data = self.cleaned_data
        name = self.cleaned_data.get('name')
        parent = self.cleaned_data.get('parent')
        
        path = os.path.join(parent, name)

        if os.access(path, os.F_OK):
            raise forms.ValidationError(_('File name already exists.'))

        return cleaned_data

class CreateLinkForm(NameForm,DirectoryFileForm):
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
