import sys
import unittest
import mock
import requests
import requests_mock

import unittests_examples

if sys.version_info >= (3,0,0):
    BUILTIN_OPEN_NAME = "builtins.open"
else:
    BUILTIN_OPEN_NAME = "__builtin__.open"

# TODO: os.environ: https://git.beercaps.ru/orlov/packer-windows-generic/blob/master/tests/test_tasks.py

class examples_UnitTests(unittest.TestCase):

    @mock.patch("unittests_examples.TestObject.do_update", return_value="patched")
    def test_do_update(self, do_update_mock):
        test_obj = unittests_examples.TestObject("member2_value")
        self.assertEqual(test_obj.member2, "member2_value")
        test_obj.update_member2()
        self.assertEqual(test_obj.member2, "patched")
        do_update_mock.return_value = "new_value"
        test_obj.update_member2()
        self.assertNotEqual(test_obj.member2, "patched")

    @mock.patch("datetime.datetime")
    def test_call_external(self, datetime_mock):
        datetime_mock.return_value = "dummy"
        test_obj = unittests_examples.TestObject("member2_value")
        test_obj.call_external()
        self.assertEqual(test_obj.member1, "dummy")
        datetime_mock.assert_called_once()
        datetime_mock.assert_called_once_with(day=31, month=12, year=2016)
        datetime_mock.reset_mock()
        datetime_mock.assert_not_called()

    def test_custom_exception(self):
        with self.assertRaises(unittests_examples.CustomException):
            unittests_examples.custom_exception()

        with self.assertRaises(unittests_examples.CustomException) as context:
            unittests_examples.custom_exception()
        self.assertTrue("This is a test" in str(context.exception))

    @requests_mock.mock()
    def test_http_request(self, req_mock):
        req_mock.request("GET", "https://www.google.com", text="some html here")
        self.assertEqual(unittests_examples.http_request("https://www.google.com").text, "some html here")

        req_mock.request(
            "GET",
            "https://www.google.com",
            json={"param1": "value1", "param2": "value2"}
        )
        self.assertEqual(unittests_examples.http_request("https://www.google.com").json(), {"param1": "value1", "param2": "value2"})
        # http://requests-mock.readthedocs.io/en/latest/history.html
        self.assertEqual(req_mock.last_request.method, "GET")
        self.assertEqual(req_mock.last_request.scheme, "https")
        self.assertEqual(req_mock.last_request.hostname, "www.google.com")
        # For multiple requests 'request_history' property could be used
        self.assertEqual(req_mock.request_history[-1].method, "GET")

        req_mock.request(
            "POST",
            "https://www.google.com/some_api",
            json={"result": "ok"}
        )
        unittests_examples.http_api_request("https://www.google.com/some_api")
        self.assertTrue("param1=1" in req_mock.last_request.url)
        self.assertTrue("param2=2" in req_mock.last_request.url)

        req_mock.request(
            "GET",
            "https://www.google.com",
            exc=requests.exceptions.ConnectTimeout("Connection timeout")
        )
        with self.assertRaises(requests.exceptions.ConnectTimeout):
            unittests_examples.http_request("https://www.google.com")

    @mock.patch(BUILTIN_OPEN_NAME, new_callable=mock.mock_open, read_data="test file data")
    def test_read_file_example(self, open_mock):
        self.assertEqual(unittests_examples.read_file_example(file_name="dummy.file"), "test file data")

    @mock.patch(BUILTIN_OPEN_NAME, new_callable=mock.mock_open)
    def test_write_file_example(self, open_mock):
        unittests_examples.write_file_example(file_name="dummy.file", file_data="new file data")
        # [!] Note open_mock(), not open_mock
        open_mock_handle = open_mock()
        open_mock_handle.write.assert_called_once_with("new file data")

    @mock.patch("subprocess.check_output")
    def test_external_process_example(self, check_output_mock):
        check_output_mock.side_effect = (u"root list".encode("utf-8"), u"home list".encode("utf-8"))
        res1, res2 = unittests_examples.external_process_example()
        self.assertEqual(res1, ["root list"])
        self.assertEqual(res2, ["home list"])

        # https://docs.python.org/3/library/unittest.mock.html
        calls = [mock.call(('ls', '/', '-lh')), mock.call('ls ~ -lh', shell=True)]
        check_output_mock.assert_has_calls(calls, any_order=True)
        check_output_mock.assert_any_call(("ls", "/", "-lh"))
        # this applies to the last call only
        check_output_mock.assert_called_with('ls ~ -lh', shell=True)

        check_output_mock.side_effect = KeyError("Test error")
        with self.assertRaises(KeyError):
            unittests_examples.external_process_example()

        # To check additional parameters of the exception a context manager needs
        # to be used
        check_output_mock.side_effect = unittests_examples.CustomException("Test error")
        with self.assertRaises(unittests_examples.CustomException) as cm:
            unittests_examples.external_process_example()

        self.assertEqual(str(cm.exception), "Test error")
