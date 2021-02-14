import pytest

# Check if moving fixtures to a separate unit also removes the warning
# pylint: disable=redefined-outer-name

@pytest.fixture(scope="function")
def function_fixture_1():
    print("\n===> fixture 1 setup")
    yield "fixture_1_resource"
    print("\n===> fixture 1 teardown")

@pytest.fixture(scope="function")
def function_fixture_2(function_fixture_1):
    print("===> fixture 2 setup")
    yield ["fixture_2_resource", function_fixture_1]
    print("\n===> fixture 2 teardown")

@pytest.fixture(scope="class")
def class_fixture_1(request):
    print("\n===> fixture 1 setup")
    request.cls.fixture_1 = "fixture_1_resource"
    yield
    print("===> fixture 1 teardown")

@pytest.fixture(scope="class")
def class_fixture_2(request):
    print("===> fixture 2 setup")
    request.cls.fixture_2 = "fixture_2_resource"
    yield
    print("\n===> fixture 2 teardown")


def test_fixture_1(function_fixture_1):
    print(f"function_fixture_1: {function_fixture_1}")

def test_fixture_2(function_fixture_2):
    print(f"function_fixture_2: {function_fixture_2}")

@pytest.mark.usefixtures("class_fixture_1", "class_fixture_2")
class TestClassFixture: # pylint: disable=too-few-public-methods
    """Class fixture test"""
    def test_both_fixtures(self):
        print(f"self.fixture_1: {self.fixture_1}") # pylint: disable=no-member
        print(f"self.fixture_2: {self.fixture_2}") # pylint: disable=no-member
