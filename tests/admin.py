from django.contrib import admin

from .models import *

admin.site.register(AdminDeleteModel)
admin.site.register(AllModel)
admin.site.register(MultipleFieldsModel)
admin.site.register(ResizeCropModel)
admin.site.register(ResizeModel)
admin.site.register(SimpleModel)
admin.site.register(ThumbnailCropModel)
admin.site.register(ThumbnailModel)
