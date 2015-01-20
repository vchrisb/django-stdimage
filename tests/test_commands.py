import os
from django.core.management import call_command
import time
from tests.models import ThumbnailModel


class TestRenderVariations(object):

    def test_no_options(self, image_upload_file):
        obj = ThumbnailModel.objects.create(image=image_upload_file)
        file_path = obj.image.thumbnail.path
        assert os.path.exists(file_path)
        os.remove(file_path)
        call_command(
            'rendervariations',
            'tests.ThumbnailModel.image'
        )
        assert os.path.exists(file_path)

    def test_no_replace(self, image_upload_file):
        obj = ThumbnailModel.objects.create(image=image_upload_file)
        file_path = obj.image.thumbnail.path
        assert os.path.exists(file_path)
        before = os.path.getmtime(file_path)
        time.sleep(1)
        call_command(
            'rendervariations',
            'tests.ThumbnailModel.image',
        )
        assert os.path.exists(file_path)
        after = os.path.getmtime(file_path)
        assert before == after

    def test_replace(self, image_upload_file):
        obj = ThumbnailModel.objects.create(image=image_upload_file)
        file_path = obj.image.thumbnail.path
        assert os.path.exists(file_path)
        before = os.path.getmtime(file_path)
        time.sleep(1)
        call_command(
            'rendervariations',
            'tests.ThumbnailModel.image',
            replace=True
        )
        assert os.path.exists(file_path)
        after = os.path.getmtime(file_path)
        assert before != after

    def test_start_at_pk(self, image_upload_file):
        obj = ThumbnailModel.objects.create(image=image_upload_file)
        file_path = obj.image.thumbnail.path
        assert os.path.exists(file_path)
        os.remove(file_path)
        obj_2 = ThumbnailModel.objects.create(image=image_upload_file)
        call_command(
            'rendervariations',
            'tests.ThumbnailModel.image@%d' % obj_2.pk,
        )
        assert not os.path.exists(file_path)
