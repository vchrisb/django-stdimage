from stdimage import fields


class TestStdImageField(object):

    def test_deprecation_warning(self, recwarn):
        fields.StdImageField()
        w = recwarn.pop(DeprecationWarning)
        assert issubclass(w.category, DeprecationWarning)
