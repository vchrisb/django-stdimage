# coding: utf-8
from __future__ import (absolute_import, unicode_literals)
from django.core.exceptions import ValidationError

import os

from django.conf import settings
from django.core.files import File
from django.test import TestCase
from django.contrib.auth.models import User

from .forms import ResizeCropModelForm, MaxSizeModelForm
from .models import SimpleModel, ResizeModel, AllModel, AdminDeleteModel, ThumbnailModel, MaxSizeModel


IMG_DIR = os.path.join(settings.MEDIA_ROOT, 'img')


class TestStdImage(TestCase):
    def setUp(self):
        User.objects.create_superuser('admin', 'admin@email.com', 'admin')
        self.client.login(username='admin', password='admin')

        self.fixtures = {}
        fixtures_dir = os.path.join(settings.MEDIA_ROOT, 'fixtures')
        fixture_paths = os.listdir(fixtures_dir)
        for fixture_filename in fixture_paths:
            fixture_path = os.path.join(fixtures_dir, fixture_filename)
            if os.path.isfile(fixture_path):
                self.fixtures[fixture_filename] = File(open(fixture_path, 'rb'))

    def tearDown(self):
        """Close all open fixtures and delete everything from media"""
        for fixture in list(self.fixtures.values()):
            fixture.close()

        for root, dirs, files in os.walk(IMG_DIR, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))


class TestModel(TestStdImage):
    """Tests model"""

    def test_simple(self):
        """Adds image and calls save."""
        instance = SimpleModel()
        instance.image = self.fixtures['100.gif']
        instance.save()
        self.assertEqual(SimpleModel.objects.count(), 1)
        self.assertEqual(SimpleModel.objects.get(pk=1), instance)
        self.assertTrue(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))

    def test_variations(self):
        """Adds image and checks filesystem as well as width and height."""
        instance = ResizeModel()
        instance.image = self.fixtures['600x400.jpg']
        instance.save()

        self.assertTrue(os.path.exists(os.path.join(IMG_DIR, 'image.jpg')))
        self.assertTrue(os.path.exists(os.path.join(IMG_DIR, 'image.thumbnail.jpg')))

        # smaller or similar size, must resolve to same file name
        # self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.medium.jpg')))

        self.assertEqual(instance.image.medium.width, 600)
        self.assertEqual(instance.image.medium.height, 400)

    def test_min_size(self):
        """Test if image matches minimal size requirements"""
        instance = AllModel()
        instance.image = self.fixtures['100.gif']
        instance.save()

        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.jpg')))


class TestModelForm(TestStdImage):
    """Tests ModelForm"""

    def test_min_size(self):
        """Test if image matches minimal size requirements"""
        form = ResizeCropModelForm({'image': self.fixtures['100.gif']})
        self.assertFalse(form.is_valid())

    def test_max_size(self):
        """Test if image matches maximal size requirements"""
        form = MaxSizeModelForm({'image': self.fixtures['600x400.jpg']})
        self.assertFalse(form.is_valid())


class TestAdmin(TestStdImage):
    """Tests admin"""

    def test_simple(self):
        """ Upload an image using the admin interface """
        self.client.post('/admin/tests/simplemodel/add/', {
            'image': self.fixtures['100.gif']
        })
        self.assertEqual(SimpleModel.objects.count(), 1)

    def test_empty_fail(self):
        """ Will raise an validation error and will not add an intance """
        self.client.post('/admin/tests/simplemodel/add/', {})
        self.assertEqual(SimpleModel.objects.count(), 0)

    def test_empty_success(self):
        """ AdminDeleteModel has blank=True and will add an instance of the Model """
        self.client.post('/admin/tests/admindeletemodel/add/', {})
        self.assertEqual(AdminDeleteModel.objects.count(), 1)

    def test_uploaded(self):
        """ Test simple upload """
        self.client.post('/admin/tests/simplemodel/add/', {
            'image': self.fixtures['100.gif']
        })
        self.assertTrue(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))

    def test_clear(self):
        """ Test if a field can be cleared """
        self.client.post('/admin/tests/admindeletemodel/add/', {
            'image': self.fixtures['100.gif']
        })
        self.client.post('/admin/tests/admindeletemodel/1/', {
            'image-clear': 'checked'
        })
        obj = AdminDeleteModel.objects.get(pk=1)
        self.assertFalse(obj.image)

    def test_delete(self):
        """ Tests if FieldFile can be deleted """
        obj = SimpleModel.objects.create(image=self.fixtures['100.gif'])
        obj.image.delete()
        self.assertFalse(obj.image)
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))

    def test_deletion_singnal_receiver(self):
        obj = SimpleModel.objects.create(image=self.fixtures['100.gif'])
        obj.delete()
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))

    def test_pre_save_delete_callback(self):
        obj = AdminDeleteModel.objects.create(image=self.fixtures['100.gif'])
        self.client.post('/admin/tests/admindeletemodel/1/', {
            'image-clear': 'checked'
        })
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))

    def test_thumbnail(self):
        """ Test if the thumbnail is there """
        self.client.post('/admin/tests/thumbnailmodel/add/', {
            'image': self.fixtures['100.gif']
        })
        self.assertTrue(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))
        self.assertTrue(os.path.exists(os.path.join(IMG_DIR, 'image.thumbnail.gif')))

    def test_delete_thumbnail(self):
        """ Delete an image with thumbnail """
        obj = ThumbnailModel.objects.create(image=self.fixtures['100.gif'])
        obj.image.delete()
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.thumbnail.gif')))

    def test_min_size(self):
        """ Tests if uploaded picture has minimal size """
        self.client.post('/admin/tests/allmodel/add/', {
            'image': self.fixtures['100.gif']
        })
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.thumbnail.gif')))


class TestValidators(TestStdImage):

    def test_max_size_validator(self):
        self.client.post('/admin/tests/maxsizemodel/add/', {
            'image': self.fixtures['600x400.jpg']
        })
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.jpg')))
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.thumbnail.jpg')))

    def test_min_size_validator(self):
        self.client.post('/admin/tests/minsizemodel/add/', {
            'image': self.fixtures['100.gif']
        })
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.gif')))
        self.assertFalse(os.path.exists(os.path.join(IMG_DIR, 'image.thumbnail.gif')))