import tempfile

from django.test import TestCase

from ..templatetags import includestatic


class TemplateTagsTest(TestCase):
    def test_read_none_file(self):
        self.assertIsNone(includestatic.read_file(None))

    def test_read_existing_file(self):
        file_content = 'temporary file for a schema-collaboration unit test'
        file = tempfile.NamedTemporaryFile(delete=False)
        file.write(file_content.encode('utf-8'))
        file.close()

        self.assertEqual(includestatic.read_file(file.name), file_content)
