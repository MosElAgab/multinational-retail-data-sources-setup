import json
from lambda_function import lambda_handler, count_number_of_stores
from unittest.mock import patch, MagicMock

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


@patch("lambda_function.boto3.client")
def test_count_number_of_stores(mock_boto3_client):
    mock_csv = "id,store_name\n1,Store A\n2,Store B\n3, Store b"
    mock_response = {
        'Body': MagicMock(read=MagicMock(return_value=mock_csv.encode("utf-8")))
    }
    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = mock_response
    mock_boto3_client.return_value = mock_s3

    count = count_number_of_stores("fake-bucket", "fake-key.csv")
    assert count == 3


@patch("lambda_function.count_number_of_stores")
def test_lambda_handler_succees(mock_count_stores, monkeypatch):
    monkeypatch.setenv("BUCKET_NAME", "some-bucket")
    monkeypatch.setenv("STORE_CSV_KEY", "some_object.csv")
    mock_count_stores.return_value = 2

    response = lambda_handler({}, {})
    body = json.loads(response["body"])

    assert response["statusCode"] == 200
    assert body["number_stores"] == 2
