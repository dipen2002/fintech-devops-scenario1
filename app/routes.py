"""Route definitions for FinTechFlow application.

Exposes web dashboard pages and RESTful operational endpoints
(/health, /version, /metrics, /api/account, /api/transactions).
"""

import logging
from typing import Any

from flask import Blueprint, current_app, jsonify, render_template, request

from app.services import (
    AccountService,
    HealthService,
    MetricsService,
    TransactionService,
)

logger = logging.getLogger("fintechflow.routes")
main_bp = Blueprint("main", __name__)


@main_bp.route("/")
def index() -> str:
    """Render the main dashboard overview page."""
    app_name = current_app.config.get("APP_NAME", "FinTechFlow")
    version = current_app.config.get("APP_VERSION", "1.0.0")
    environment = current_app.config.get("ENVIRONMENT", "development")

    account = AccountService.get_account_summary()
    transactions = TransactionService.get_transactions()[:4]
    stats = TransactionService.get_transaction_statistics()
    health = HealthService.get_health_status(version, environment)

    logger.debug("Dashboard loaded for environment: %s", environment)
    return render_template(
        "index.html",
        app_name=app_name,
        version=version,
        environment=environment,
        account=account,
        transactions=transactions,
        stats=stats,
        health=health,
    )


@main_bp.route("/account")
def account() -> str:
    """Render the mock account details and summary page."""
    app_name = current_app.config.get("APP_NAME", "FinTechFlow")
    version = current_app.config.get("APP_VERSION", "1.0.0")
    environment = current_app.config.get("ENVIRONMENT", "development")

    account_data = AccountService.get_account_summary()
    stats = TransactionService.get_transaction_statistics()

    logger.debug("Account page requested for %s", account_data.get("account_holder"))
    return render_template(
        "account.html",
        app_name=app_name,
        version=version,
        environment=environment,
        account=account_data,
        stats=stats,
    )


@main_bp.route("/transactions")
def transactions() -> str:
    """Render the mock transaction history feed."""
    app_name = current_app.config.get("APP_NAME", "FinTechFlow")
    version = current_app.config.get("APP_VERSION", "1.0.0")
    environment = current_app.config.get("ENVIRONMENT", "development")

    all_txs = TransactionService.get_transactions()
    stats = TransactionService.get_transaction_statistics()

    logger.debug("Transactions page requested, displaying %d entries", len(all_txs))
    return render_template(
        "transactions.html",
        app_name=app_name,
        version=version,
        environment=environment,
        transactions=all_txs,
        stats=stats,
    )


# ==============================================================================
# Operational & DevOps Endpoints
# ==============================================================================


@main_bp.route("/health", methods=["GET"])
def health() -> Any:
    """Health check endpoint used by Docker HEALTHCHECK, CI/CD, and load balancers.

    Returns JSON conforming to standard container health checks.
    """
    version = current_app.config.get("APP_VERSION", "1.0.0")
    environment = current_app.config.get("ENVIRONMENT", "development")
    health_payload = HealthService.get_health_status(version, environment)

    logger.info("Health check requested - status: %s", health_payload["status"])
    return jsonify(health_payload), 200


@main_bp.route("/version", methods=["GET"])
def version() -> Any:
    """Application version endpoint for deployment verification and smoke tests."""
    app_name = current_app.config.get("APP_NAME", "FinTechFlow")
    app_version = current_app.config.get("APP_VERSION", "1.0.0")
    environment = current_app.config.get("ENVIRONMENT", "development")

    return jsonify(
        {
            "service": app_name,
            "version": app_version,
            "environment": environment,
        }
    ), 200


@main_bp.route("/metrics", methods=["GET"])
def metrics() -> Any:
    """Lightweight application metrics endpoint for observability demonstration."""
    metrics_data = MetricsService.get_metrics()
    logger.debug("Metrics exported: %s requests recorded", metrics_data["total_requests"])
    return jsonify(metrics_data), 200


# ==============================================================================
# Mock REST API Endpoints (Educational Demonstration)
# ==============================================================================


@main_bp.route("/api/account", methods=["GET"])
def api_account() -> Any:
    """REST API endpoint returning simulated demo account summary."""
    return jsonify(AccountService.get_account_summary()), 200


@main_bp.route("/api/transactions", methods=["GET"])
def api_transactions() -> Any:
    """REST API endpoint returning simulated demo transaction history."""
    category = request.args.get("category")
    txs = TransactionService.get_transactions()
    if category:
        txs = [t for t in txs if t["category"].lower() == category.lower()]
    return jsonify({"transactions": txs, "count": len(txs), "is_demo": True}), 200
