from . import demo_algo


def test_sentiment():
    algo_response = demo_algo.apply("I am glad I bought this guitar, it's perfect!")
    assert algo_response["sentiment"] == 1


def test_model_metadata():
    algo_response = demo_algo.apply("dummy input")
    assert "predicting_model_metadata" in algo_response
