"""Additional route, middleware, error handling, and configuration tests."""

from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import (
    DevelopmentConfig,
    ProductionConfig,
    StagingConfig,
    TestingConfig,
    get_config,
)
from app.services import HealthService


def test_home_page_renders_successfully(client: FlaskClient) -> None:
    """Verify GET / returns HTTP 200 and displays application name and dashboard."""
    response = client.get("/")
    assert response.status_code == 200

    html = response.get_data(as_text=True)
    assert "FinTechFlow" in html
    assert "Dashboard" in html
    assert "Release Version" in html


def test_invalid_route_returns_404_html(client: FlaskClient) -> None:
    """Verify accessing an invalid web page returns HTTP 404 HTML template."""
    response = client.get("/non-existent-page-url")
    assert response.status_code == 404
    html = response.get_data(as_text=True)
    assert "404" in html
    assert "Page Not Found" in html


def test_invalid_api_route_returns_404_json(client: FlaskClient) -> None:
    """Verify accessing an invalid API endpoint returns structured JSON 404."""
    response = client.get("/api/non-existent-endpoint")
    assert response.status_code == 404
    assert response.is_json
    data = response.get_json()
    assert data is not None
    assert data["error"] == "Not Found"
    assert data["status_code"] == 404


def test_metrics_endpoint_records_requests(client: FlaskClient) -> None:
    """Verify GET /metrics returns accurate request counts and tracks requests."""
    # Issue several requests
    client.get("/health")
    client.get("/version")
    client.get("/non-existent-route")  # 404

    metrics_res = client.get("/metrics")
    assert metrics_res.status_code == 200
    assert metrics_res.is_json

    metrics_data = metrics_res.get_json()
    assert metrics_data is not None
    assert metrics_data["service"] == "FinTechFlow"
    assert metrics_data["total_requests"] >= 3
    assert metrics_data["successful_requests"] >= 2
    assert metrics_data["failed_requests"] >= 1
    assert "uptime_seconds" in metrics_data


def test_security_headers_present_in_response(client: FlaskClient) -> None:
    """Verify mandatory security headers are applied to HTTP responses."""
    response = client.get("/health")
    assert response.headers.get("X-Content-Type-Options") == "nosniff"
    assert response.headers.get("X-Frame-Options") == "DENY"
    assert response.headers.get("X-XSS-Protection") == "1; mode=block"
    assert "Content-Security-Policy" in response.headers


def test_configuration_environments() -> None:
    """Verify configuration profile mapping logic."""
    assert get_config("development") == DevelopmentConfig
    assert get_config("dev") == DevelopmentConfig
    assert get_config("staging") == StagingConfig
    assert get_config("stage") == StagingConfig
    assert get_config("production") == ProductionConfig
    assert get_config("prod") == ProductionConfig
    assert get_config("testing") == TestingConfig
    assert get_config("unknown-env") == DevelopmentConfig


def test_health_service_evaluation() -> None:
    """Unit test for HealthService."""
    res = HealthService.get_health_status("1.0.0", "staging")
    assert res["status"] == "healthy"
    assert res["version"] == "1.0.0"
    assert res["environment"] == "staging"


def test_create_app_without_arguments() -> None:
    """Verify application factory creates an app with default configuration."""
    app = create_app()
    assert isinstance(app, Flask)
    assert app.config["APP_NAME"] == "FinTechFlow"
