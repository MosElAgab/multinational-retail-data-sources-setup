import json
from get_store.lambda_function import lambda_handler


def test_lambda_handler_missing_env(monkeypatch):
    # delete env variables
    monkeypatch.delenv("BUCKET_NAME", raising=False)
    monkeypatch.delenv("STORE_CSV_KEY", raising=False)

    # response
    response = lambda_handler({}, {})
    body = json.loads(response["body"])

    # assert
    assert response["statusCode"] == 500
    assert "missing env" in body["message"]
