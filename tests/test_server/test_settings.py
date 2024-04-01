import json

from fastapi.testclient import TestClient
from httpx import Response
from starlette import status

from modules.server import app

client = TestClient(app)


def get_content(response: Response) -> dict:
    return json.loads(response.content.decode())


def test_get_config():
    response = client.get("/settings")
    content = get_content(response)
    assert response.status_code == status.HTTP_200_OK
    assert content.get("CONFIG_NAME") == "config.ini"


def test_update_config_err():
    payload = {"OPENAI_API_KEY": "NONE"}
    payload = json.dumps(payload)
    response = client.post("/settings", content=payload)
    assert response.status_code == status.HTTP_400_BAD_REQUEST
