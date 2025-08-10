import json
from get_store.lambda_function import lambda_handler, get_store_data, get_store_by_row_index
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


@patch("get_store.lambda_function.boto3.client")
def test_get_store_data(mock_boto3_client):
    mock_csv = "id,store_name\n1,Store A\n2,Store B\n3, Store b"
    mock_response = {
        'Body': MagicMock(read=MagicMock(return_value=mock_csv.encode("utf-8")))
    }
    mock_s3 = MagicMock()
    mock_s3.get_object.return_value = mock_response
    mock_boto3_client.return_value = mock_s3
    
    data = get_store_data("fake-bucket", "fake-key.csv")
    assert isinstance(data, list)

@patch("get_store.lambda_function.get_store_data")
def test_get_store_by_row_index(mock_get_store_data):
    mock_get_store_data.return_value = [
        {"store_name": "Store A"},
        {"store_name": "Store B"},
        {"store_name": "Store C"}
    ]
    store_by_row_index = get_store_by_row_index("fake-bucket", "fake-key.csv", 1)
    assert store_by_row_index["store_name"] == "Store B"