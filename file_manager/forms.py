from django import forms

class DirectoryForm(forms.Form):
    parent = forms.FilePathField(path='/')
    name = forms.CharField()

class FileForm(forms.Form):
    parent = forms.CharField()
    name = forms.CharField()
    content = forms.CharField()

class UploadForm(forms.Form):
    parent = forms.CharField()
    name = forms.CharField()
    content = forms.CharField()

