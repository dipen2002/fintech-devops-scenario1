"""Domain services for FinTechFlow educational demonstration.

Provides mock data sources and in-memory operational metrics.
IMPORTANT: All financial data in this module is simulated DEMO DATA.
"""

import threading
import time
from datetime import UTC, datetime
from typing import Any


class AccountService:
    """Provides mock account information for demonstration purposes."""

    @staticmethod
    def get_account_summary() -> dict[str, Any]:
        """Return demo account summary.

        NOTE: All data returned is strictly synthetic educational mock data.
        """
        return {
            "account_holder": "Demo User",
            "account_type": "Personal Current Account",
            "account_number": "DEMO-GB-8821-4902",
            "sort_code": "20-00-00 (DEMO)",
            "balance": 5250.00,
            "currency": "GBP",
            "currency_symbol": "£",
            "formatted_balance": "£5,250.00",
            "status": "Active",
            "overdraft_limit": 500.00,
            "is_demo_data": True,
            "disclaimer": "EDUCATIONAL DEMO ONLY - NO REAL FINANCIAL INTEGRATION",
            "last_updated": datetime.now(UTC).strftime("%Y-%m-%d %H:%M:%S UTC"),
        }


class TransactionService:
    """Provides mock transaction list for demonstration purposes."""

    _MOCK_TRANSACTIONS: list[dict[str, Any]] = [
        {
            "id": "TXN-DEMO-001",
            "title": "Grocery Store",
            "category": "Groceries",
            "amount": -45.50,
            "formatted_amount": "-£45.50",
            "type": "debit",
            "date": "2026-08-28 14:32",
            "status": "Completed",
            "reference": "STORE-PURCHASE-DEMO",
        },
        {
            "id": "TXN-DEMO-002",
            "title": "Salary",
            "category": "Income",
            "amount": 2500.00,
            "formatted_amount": "+£2,500.00",
            "type": "credit",
            "date": "2026-08-27 09:00",
            "status": "Completed",
            "reference": "PAYROLL-MONTHLY-DEMO",
        },
        {
            "id": "TXN-DEMO-003",
            "title": "Electricity",
            "category": "Utilities",
            "amount": -85.20,
            "formatted_amount": "-£85.20",
            "type": "debit",
            "date": "2026-08-25 11:15",
            "status": "Completed",
            "reference": "ENERGY-DIRECT-DEBIT",
        },
        {
            "id": "TXN-DEMO-004",
            "title": "Coffee Shop",
            "category": "Dining",
            "amount": -4.50,
            "formatted_amount": "-£4.50",
            "type": "debit",
            "date": "2026-08-24 08:45",
            "status": "Completed",
            "reference": "CAFE-CARD-PAYMENT",
        },
        {
            "id": "TXN-DEMO-005",
            "title": "Freelance Consulting",
            "category": "Income",
            "amount": 450.00,
            "formatted_amount": "+£450.00",
            "type": "credit",
            "date": "2026-08-22 16:20",
            "status": "Completed",
            "reference": "CLIENT-INVOICE-104",
        },
        {
            "id": "TXN-DEMO-006",
            "title": "Broadband Internet",
            "category": "Utilities",
            "amount": -38.00,
            "formatted_amount": "-£38.00",
            "type": "debit",
            "date": "2026-08-20 10:00",
            "status": "Completed",
            "reference": "TELECOM-MONTHLY-SUB",
        },
    ]

    @classmethod
    def get_transactions(cls) -> list[dict[str, Any]]:
        """Return the list of simulated demo transactions."""
        return [dict(tx) for tx in cls._MOCK_TRANSACTIONS]

    @classmethod
    def get_transaction_statistics(cls) -> dict[str, Any]:
        """Calculate basic summary statistics over the mock transactions."""
        txs = cls._MOCK_TRANSACTIONS
        total_income = sum(t["amount"] for t in txs if t["amount"] > 0)
        total_expenses = abs(sum(t["amount"] for t in txs if t["amount"] < 0))
        return {
            "total_transactions": len(txs),
            "total_income": total_income,
            "formatted_income": f"+£{total_income:,.2f}",
            "total_expenses": total_expenses,
            "formatted_expenses": f"-£{total_expenses:,.2f}",
            "net_flow": total_income - total_expenses,
            "formatted_net_flow": f"£{(total_income - total_expenses):,.2f}",
            "is_demo_data": True,
        }


class MetricsService:
    """Thread-safe in-memory metrics collector for educational observability."""

    _lock = threading.Lock()
    _total_requests: int = 0
    _successful_requests: int = 0
    _failed_requests: int = 0
    _endpoint_hits: dict[str, int] = {}
    _start_time: float = time.time()

    @classmethod
    def record_request(cls, endpoint: str, status_code: int) -> None:
        """Record an incoming request and its resulting HTTP status code."""
        with cls._lock:
            cls._total_requests += 1
            if status_code < 400:
                cls._successful_requests += 1
            else:
                cls._failed_requests += 1

            endpoint_key = endpoint or "unknown"
            cls._endpoint_hits[endpoint_key] = (
                cls._endpoint_hits.get(endpoint_key, 0) + 1
            )

    @classmethod
    def get_metrics(cls) -> dict[str, Any]:
        """Retrieve current in-memory metrics snapshot."""
        with cls._lock:
            uptime = round(time.time() - cls._start_time, 2)
            return {
                "service": "FinTechFlow",
                "uptime_seconds": uptime,
                "total_requests": cls._total_requests,
                "successful_requests": cls._successful_requests,
                "failed_requests": cls._failed_requests,
                "endpoint_hits": dict(cls._endpoint_hits),
                "timestamp": datetime.now(UTC).isoformat(),
                "note": "Demonstration in-memory metrics only - not production APM.",
            }

    @classmethod
    def reset_metrics(cls) -> None:
        """Reset metrics (primarily used in test teardowns)."""
        with cls._lock:
            cls._total_requests = 0
            cls._successful_requests = 0
            cls._failed_requests = 0
            cls._endpoint_hits.clear()
            cls._start_time = time.time()


class HealthService:
    """Service to evaluate system health status."""

    @staticmethod
    def get_health_status(app_version: str, environment: str) -> dict[str, Any]:
        """Evaluate and return application health status."""
        return {
            "status": "healthy",
            "service": "FinTechFlow",
            "version": app_version,
            "environment": environment,
            "timestamp": datetime.now(UTC).isoformat(),
        }
