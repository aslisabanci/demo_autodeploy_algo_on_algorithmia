from . import demo_jameskenny

def test_demo_jameskenny():
    assert demo_jameskenny.apply("Jane") == "hello Jane"
