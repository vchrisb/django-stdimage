# -*- coding: utf-8 -*-
from __future__ import (absolute_import, unicode_literals)

import os
import uuid
from .models import StdImageField


def upload_to(name, ext, path=''):
    return os.path.join(path, '%s.%s' % (name, ext)).lower()


def upload_to_uuid(instance, filename, path=''):
    ext = filename.rsplit('.', 1)[-1]
    return upload_to(uuid.uuid4().hex, ext, path)


def upload_to_class_name_dir(instance, filename, name=''):
    ext = filename.rsplit('.', 1)[-1]
    if name == '':
        name = filename.rsplit('/', 1)[-1]
    class_name = instance.__class__.__name__
    return upload_to(name, ext, class_name)


def upload_to_class_name_dir_uuid(instance, filename):
    return upload_to_class_name_dir(instance, filename, uuid.uuid4().hex)


def pre_delete_delete_callback(sender, instance, **kwargs):
    for field in instance._meta.fields:
        if isinstance(field, StdImageField):
            getattr(instance, field.name).delete()


def pre_save_delete_callback(sender, instance, **kwargs):
    if instance.pk:
        obj = sender.objects.get(pk=instance.pk)
        for field in instance._meta.fields:
            if isinstance(field, StdImageField):
                obj_field = getattr(obj, field.name)
                instance_field = getattr(instance, field.name)
                if obj_field and not instance_field:
                    obj_field.delete(False)
