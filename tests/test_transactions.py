"""Automated test cases for transaction feed views and APIs.

Verifies that mock transactions (Grocery Store, Salary, Electricity,
Coffee Shop, etc.) render properly and calculate correct statistics.
"""

from flask.testing import FlaskClient

from app.services import TransactionService


def test_transactions_page_renders_successfully(client: FlaskClient) -> None:
    """Verify GET /transactions returns HTTP 200 and displays expected sample transactions."""
    response = client.get("/transactions")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert "Grocery Store" in html
    assert "Salary" in html
    assert "Electricity" in html
    assert "Coffee Shop" in html
    assert "Transaction History" in html


def test_transactions_api_endpoint(client: FlaskClient) -> None:
    """Verify GET /api/transactions returns JSON array of transactions."""
    response = client.get("/api/transactions")
    assert response.status_code == 200
    assert response.is_json

    data = response.get_json()
    assert data is not None
    assert "transactions" in data
    assert data["count"] > 0
    assert data["is_demo"] is True

    titles = [t["title"] for t in data["transactions"]]
    assert "Grocery Store" in titles
    assert "Salary" in titles
    assert "Electricity" in titles
    assert "Coffee Shop" in titles


def test_transactions_api_category_filter(client: FlaskClient) -> None:
    """Verify category filtering on GET /api/transactions."""
    response = client.get("/api/transactions?category=Utilities")
    assert response.status_code == 200
    data = response.get_json()

    assert data is not None
    for tx in data["transactions"]:
        assert tx["category"] == "Utilities"


def test_transaction_service_statistics() -> None:
    """Unit test for TransactionService statistics calculation."""
    stats = TransactionService.get_transaction_statistics()
    assert stats["total_transactions"] >= 4
    assert stats["total_income"] > 0
    assert stats["total_expenses"] > 0
    assert stats["is_demo_data"] is True
