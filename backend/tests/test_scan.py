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
        filepath = f.name  
    
    try:
        with open(filepath, "rb") as file:
            data = {"file": (file, "hello.py")}
            response = client.post("/scan", content_type="multipart/form-data", data=data)

        print("Response status:", response.status_code)
        print("Response JSON:", response.json)

        assert response.status_code == 200
        assert isinstance(response.json, list)

    except Exception as e:
        print("🔥 Test failed with exception:", e)
        raise

    finally:
        if os.path.exists(filepath):
            os.unlink(filepath)

def test_example():
    print("🔥 Test started")
    assert 1 == 2
