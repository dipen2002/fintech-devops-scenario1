"""Automated test cases for the account summary views and APIs.

Verifies that mock account details, demo balance, and educational
disclaimers render properly.
"""

from flask.testing import FlaskClient


def test_account_page_renders_successfully(client: FlaskClient) -> None:
    """Verify GET /account returns HTTP 200 and displays demo user information."""
    response = client.get("/account")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert "Demo User" in html
    assert "£5,250.00" in html
    assert "Active" in html
    assert "MOCK ACCOUNT DATA" in html or "EDUCATIONAL DEMO" in html


def test_account_api_endpoint(client: FlaskClient) -> None:
    """Verify GET /api/account returns valid JSON summary with demo disclaimer."""
    response = client.get("/api/account")
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data is not None
    assert data["account_holder"] == "Demo User"
    assert data["balance"] == 5250.00
    assert data["currency"] == "GBP"
    assert data["is_demo_data"] is True
    assert "disclaimer" in data
