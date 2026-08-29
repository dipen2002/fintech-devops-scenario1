"""Automated test cases for the /version endpoint.

Verifies that the release version endpoint returns expected versioning
data for deployment smoke tests and automated verification scripts.
"""

from flask import Flask
from flask.testing import FlaskClient


def test_version_endpoint_status_code(client: FlaskClient) -> None:
    """Verify GET /version returns HTTP 200 OK."""
    response = client.get("/version")
    assert response.status_code == 200


def test_version_endpoint_payload(app: Flask, client: FlaskClient) -> None:
    """Verify GET /version returns matching version string and service name."""
    response = client.get("/version")
    assert response.is_json

    data = response.get_json()
    assert data is not None
    assert data["service"] == "FinTechFlow"
    assert data["version"] == app.config["APP_VERSION"]
    assert data["environment"] == "testing"
