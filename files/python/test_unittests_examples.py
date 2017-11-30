import sys
import unittest
import mock

import unittests_examples

if sys.version_info >= (3,0,0):
    BUILTIN_OPEN_NAME = "builtins.open"
else:
    BUILTIN_OPEN_NAME = "__builtin__.open"

class examples_UnitTests(unittest.TestCase):

    @mock.patch(BUILTIN_OPEN_NAME, new_callable=mock.mock_open, read_data="test file data")
    def test_read_file_example(self, open_mock):
        self.assertEqual(unittests_examples.read_file_example(file_name="dummy.file"), "test file data")

    @mock.patch(BUILTIN_OPEN_NAME, new_callable=mock.mock_open)
    def test_write_file_example(self, open_mock):
        unittests_examples.write_file_example(file_name="dummy.file", file_data="new file data")
        # [!] Note open_mock(), not open_mock
        open_mock_handle = open_mock()
        open_mock_handle.write.assert_called_once_with("new file data")
