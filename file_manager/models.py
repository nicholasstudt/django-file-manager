from django.db import models
from django.contrib import admin

class File(models.Model):
    class Meta:
        permissions = (
            ("can_create", "Can create file"),
            ("can_update", "Can update file"),
            ("can_copy", "Can copy file"),
            ("can_upload", "Can upload file"),
            ("can_delete", "Can delete file"),
            ("can_rename", "Can rename file"),
        )

class Directory(models.Model):
    class Meta:
        verbose_name_plural = "Directories"
        permissions = (
            ("can_copy", "Can copy directory"),
            ("can_delete", "Can delete directory"),
            ("can_rename", "Can rename directory"),
            ("can_mkdir", "Can make directory"),
        )
