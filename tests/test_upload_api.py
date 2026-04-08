
import io
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(__file__)))

from app import app

def test_icon_upload():
    client = app.test_client()

    data = {
        "icon": (io.BytesIO(b"fake image"), "test.png")
    }

    response = client.post(
        "/api/upload/icon",
        data=data,
        content_type="multipart/form-data"
    )

    assert response.status_code in [200, 400]