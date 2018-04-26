import datetime
import requests

class CustomException(Exception):
    pass

class TestObject(object):
    member1 = "member1_value"

    def __init__(self, member2):
        self.member2 = member2

    def update_member2(self):
        self.member2 = self.do_update()

    def do_update(self):
        return "new_value"

    def call_external(self):
        self.member1 = datetime.datetime(year=2016, month=12, day=31)

def custom_exception():
    raise CustomException("This is a test")

def http_request(url):
    return requests.get(url)

def read_file_example(file_name):
    with open(file_name, "r") as f:
        file_contents = f.read()
    return(file_contents)

def write_file_example(file_name, file_data):
    with open(file_name, "w") as f:
        f.write(file_data)