.. image:: https://travis-ci.org/codingjoe/django-stdimage.png
  :target: https://travis-ci.org/codingjoe/django-stdimage
.. image:: https://pypip.in/v/django-stdimage/badge.png
  :target: https://crate.io/packages/django-stdimage
.. image:: https://pypip.in/d/django-stdimage/badge.png
  :target: https://crate.io/packages/django-stdimage
.. image:: https://pypip.in/license/django-stdimage/badge.png
  :target: https://pypi.python.org/pypi/django-stdimage/

Django Standarized Image Field
==============================

Django Field that implement the following features:

* Django-Storages compatible (S3)
* Python 2 & 3 support
* Resize images to different sizes
* Access thumbnails on model level, no template tags required
* Preserves original image
* Restrict accepted image dimensions
* Rename files to a standardized name (using a callable upload_to)

Installation
------------

Install latest PIL - there is really no reason to use this package without it

`easy_install django-stdimage`

or

`pip django-stdimage`

Put `'stdimage'` in the INSTALLED_APPS

Usage
-----

Import it in your project, and use in your models.

Example::

    from stdimage import StdImageField

    class MyModel(models.Model):
        ## works as ImageField
        image1 = StdImageField(upload_to='path/to/img')

        ## can be deleted through admin
        image2 = StdImageField(upload_to='path/to/img', blank=True)

        ## creates a thumbnail resized to maximum size to fit a 100x75 area
        # the original call
        image3 = StdImageField(upload_to='path/to/img', thumbnail_size=(100, 75))
        # is the same as intermediate-style call
        image3 = StdImageField(upload_to='path/to/img', variations={'thumbnail': (100, 75)})
        # is the same as the new-style-call
        image3 = StdImageField(upload_to='path/to/img', variations={'thumbnail': {"width": 100, "height": 75})

        ## creates a thumbnail resized to 100x100 croping if necessary
        image4 = StdImageField(upload_to='path/to/img', variations={'thumbnail': (100, 100, True)})
        # or the new style
        image4 = StdImageField(upload_to='path/to/img', variations={'thumbnail': {"width": 100, "height": 100, "crop":True}})

        ## creates a thumbnail resized to 100x100 croping if necessary and excepts only image greater than 1920x1080px
        ## if min_size is not specified, it won't accept smaller than the smallest variation image
        image5 = StdImageField(upload_to='path/to/img', variations={'thumbnail': (100, 100, True)}, min_size=(1920, 1080))

        ## Full ammo here. Please note all the definitions below are equal
        image_all = StdImageField(upload_to=upload_to, blank=True,
                               variations={'large': (600, 400), 'thumbnail': (100, 100, True), 'resized': (300, 200)})

For using generated thumbnail in templates use "myimagefield.thumbnail". Example::

    <a href="{{ object.myimage.url }}"><img alt="" src="{{ object.myimage.thumbnail.url }}"/></a>

About image names
-----------------

By default StdImageField stores images without modifying the file name. If you want to use more consistent file names you can use the build in upload functions.
Example::

    from stdimage import StdImageField, upload_to_uuid, upload_to_class_name_dir, upload_to_class_name_dir_uuid
    from functools import partial

    class MyClass(models.Model)
        # Gets saved to MEDIA_ROOT/myclass/#FILENAME#.#EXT#
        image1 = StdImageField(upload_to=upload_to_class_name)

        # Gets saved to MEDIA_ROOT/myclass/pic.#EXT#
        image2 = StdImageField(upload_to=partial(upload_to_class_name, name='pic'))

        # Gets saved to MEDIA_ROOT/images/#UUID#.#EXT#
        image3 = StdImageField(upload_to=partial(upload_to_uuid, path='images'))

        # Gets saved to MEDIA_ROOT/myclass/#UUID#.#EXT#
        image4 = StdImageField(upload_to=upload_to_class_name_dir_uuid)


You can restrict the upload dimension of images using `min_size` and `max_size`. Both arguments accept a (width, height) tuple. By default, the minimum resolution is set to the biggest variation.
CAUTION: The `max_size` should be used with caution. As storage isn't expensive, you shouldn't restrict upload dimensions. If you seek prevent users form overflowing your memory you should restrict the HTTP upload body size.

Deleting images
---------------

Django `dropped support
<https://docs.djangoproject.com/en/dev/releases/1.3/#deleting-a-model-doesn-t-delete-associated-files>`_. for automated deletions in version 1.3.
Implementing file deletion `should be done
<http://stackoverflow.com/questions/5372934/how-do-i-get-django-admin-to-delete-files-when-i-remove-an-object-from-the-datab>`_. inside your own applications using the `post_delete` or `pre_delete` signal.
Clearing the field if blank is true, does not delete the file. This can also be achieved using `pre_save` and `post_save` signals.
This packages contains two signal callback methods that handle file deletion for all SdtImageFields of a model.::

    from stdimage import pre_delete_delete_callback, pre_save_delete_callback

    post_delete.connect(pre_delete_delete_callback, sender=MyModel)
    pre_save.connect(pre_save_delete_callback, sender=MyModel)


Warning: You should not use the singal callbacks in production. They may result in data loss.


Testing
-------
To run the tests simply run::

    python setup.py test

