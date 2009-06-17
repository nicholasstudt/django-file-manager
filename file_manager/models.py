from django.db import models
from django.contrib import admin

class Objects(models.Model):
    class Meta:
        permissions = (
            ("can_create", "Can create file"),
            ("can_update", "Can update file"),
            ("can_copy", "Can copy file/directory"),
            ("can_upload", "Can upload file"),
            ("can_delete", "Can delete file/directory"),
            ("can_rename", "Can rename file/directory"),
            ("can_mkdir", "Can make directory"),
        )
#admin.site.register(Objects)

