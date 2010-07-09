from django.contrib.auth.models import User
from django.db import models
from django.utils.translation import ugettext as _
#from django.contrib import admin

class File(models.Model):
    TYPES = (
        ('S_IFSOCK', _('Socket')),
        ('S_IFLNK', _('Symbolic link')),
        ('S_IFREG', _('Regular file')),
        ('S_IFBLK', _('Block device')),
        ('S_IFDIR', _('Directory')),
        ('S_IFCHR', _('Character device')),
        ('S_IFIFO', _('FIFO')),
    )

    # Path is relative to settings.DOCUMENT_ROOT
    path = models.TextField()
    name = models.CharField(max_length=250)  
    type = models.CharField(max_length=10, choices=TYPES)
   
    # By default the person that created the file.
    owner = models.ForeignKey(User) 

    # How should permissions be handled?
    # What can a non-owner do? What can they not do?
    # How is that represented?

    #permissions = models.ManyToManyField(Permission, verbose_name=_('file permissions'), blank=True)

    class Meta:
        permissions = (
            ('can_create_file', _('Can create file')),
            ('can_update_file', _('Can update file')),
            ('can_copy_file', _('Can copy file')),
            ('can_upload_file', _('Can upload file')),
            ('can_delete_file', _('Can delete file')),
            ('can_rename_file', _('Can rename file')),
            ('can_move_file', _('Can move file')),

            ('can_create_symlink', _('Can create symlink')),
            ('can_copy_symlink', _('Can copy symlink')),
            ('can_move_symlink', _('Can move symlink')),
            ('can_rename_symlink', _('Can rename symlink')),
            ('can_delete_symlink', _('Can delete symlink')),

            ('can_copy_dir', _('Can copy directory')),
            ('can_delete_dir', _('Can delete directory')),
            ('can_rename_dir', _('Can rename directory')),
            ('can_create_dir', _('Can make directory')),
            ('can_move_dir', _('Can move directory')),


        )
