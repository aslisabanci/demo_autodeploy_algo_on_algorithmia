from . import demo_gh


def test_sentiment():
    algo_response = demo_gh.apply("I am glad I bought this guitar, it's perfect!")
    assert algo_response["sentiment"] == 1


def test_model_metadata():
    algo_response = demo_gh.apply("dummy input")
    assert "predicting_model_metadata" in algo_response