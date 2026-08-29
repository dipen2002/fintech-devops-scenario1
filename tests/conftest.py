"""Pytest fixtures for FinTechFlow automated test suite."""

import pytest
from flask import Flask
from flask.testing import FlaskClient

from app import create_app
from app.config import TestingConfig
from app.services import MetricsService


@pytest.fixture
def app() -> Flask:
    """Create and configure a Flask application instance for testing."""
    app_instance = create_app(TestingConfig)
    # Reset metrics before each test to guarantee test isolation
    MetricsService.reset_metrics()
    return app_instance


@pytest.fixture
def client(app: Flask) -> FlaskClient:
    """Create a test client for executing HTTP requests against the application."""
    return app.test_client()
