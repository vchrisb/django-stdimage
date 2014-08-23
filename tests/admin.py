from django.contrib import admin

from .models import *

admin.site.register(AdminDeleteModel)
admin.site.register(ResizeCropModel)
admin.site.register(ResizeModel)
admin.site.register(SimpleModel)
admin.site.register(ThumbnailModel)
admin.site.register(MaxSizeModel)
admin.site.register(MinSizeModel)
admin.site.register(ForceMinSizeModel)
