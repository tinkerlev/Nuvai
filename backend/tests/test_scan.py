import os
import tempfile
import pytest
from server import app

@pytest.fixture
def client():
    app.config["TESTING"] = True
    with app.test_client() as client:
        yield client

def test_scan_valid_python_file(client):
    code = "def hello():\n    print('Hello')"
    with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w") as f:
        f.write(code)
        f.seek(0)

        try:
            with open(f.name, "rb") as file:
                data = {"file": (file, f.name)}
                response = client.post("/scan", content_type="multipart/form-data", data=data)

            print("Response status:", response.status_code)
            print("Response JSON:", response.json)

            assert response.status_code == 200
            assert isinstance(response.json, list)

        except Exception as e:
            print("🔥 Test failed with exception:", e)
            raise
        finally:
            os.unlink(f.name)

def test_example():
    print("🔥 Test started")
    assert 1 == 2
