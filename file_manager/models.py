from django.db import models
from django.contrib import admin

class Items(models.Model):
    class Meta:
        permissions = (
            ("can_create_file", "Can create file"),
            ("can_update_file", "Can update file"),
            ("can_copy_file", "Can copy file"),
            ("can_upload_file", "Can upload file"),
            ("can_delete_file", "Can delete file"),
            ("can_rename_file", "Can rename file"),
            ("can_move_file", "Can move file"),

            ("can_copy_dir", "Can copy directory"),
            ("can_delete_dir", "Can delete directory"),
            ("can_rename_dir", "Can rename directory"),
            ("can_create_dir", "Can make directory"),
            ("can_move_dir", "Can move directory"),
        )
