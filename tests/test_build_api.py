import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import json
from app import app


def test_build_endpoint():
    client = app.test_client()

    payload = {
        "app_name": "TestApp",
        "app_description": "Demo",
        "app_version": "1.0",
        "build_number": "1",
        "package_name": "com.test.app",
        "web_url": "https://example.com",
        "platforms": ["android"]
    }

    response = client.post(
        "/api/build",
        data=json.dumps(payload),
        content_type="application/json"
    )

    assert response.status_code == 200
    assert "build_id" in response.get_json()