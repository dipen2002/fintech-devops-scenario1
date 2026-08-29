"""Automated test cases for the /health endpoint.

Verifies that container health checks and deployment gates receive
expected HTTP 200 responses and healthy status payloads.
"""

from flask.testing import FlaskClient


def test_health_endpoint_status_code(client: FlaskClient) -> None:
    """Verify GET /health returns HTTP 200 OK."""
    response = client.get("/health")
    assert response.status_code == 200


def test_health_endpoint_json_structure(client: FlaskClient) -> None:
    """Verify GET /health returns JSON with status='healthy' and correct metadata."""
    response = client.get("/health")
    assert response.is_json

    data = response.get_json()
    assert data is not None
    assert data["status"] == "healthy"
    assert data["service"] == "FinTechFlow"
    assert "version" in data
    assert "environment" in data
    assert "timestamp" in data
