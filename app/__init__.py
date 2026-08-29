"""FinTechFlow Flask Application Factory.

Initializes the Flask application with environment-specific configuration,
logging, request observability middleware, error handlers, and security headers.
"""

import logging
import sys
import time
from typing import Any

from flask import Flask, Response, g, jsonify, render_template, request

from app.config import Config, get_config
from app.services import MetricsService


def configure_logging(log_level_name: str) -> None:
    """Configure structured logging output to standard streams."""
    log_level = getattr(logging, log_level_name.upper(), logging.INFO)

    formatter = logging.Formatter(
        fmt="[%(asctime)s] [%(levelname)s] [%(name)s] %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)

    # Avoid duplicate handlers during factory calls
    if not root_logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        root_logger.addHandler(handler)
    else:
        for handler in root_logger.handlers:
            handler.setFormatter(formatter)


def create_app(config_class: type[Config] | None = None) -> Flask:
    """Application factory for FinTechFlow.

    Args:
        config_class: Optional configuration class. If omitted, uses get_config().

    Returns:
        Configured Flask application instance.
    """
    app = Flask(__name__)

    # Load configuration
    if config_class is None:
        config_class = get_config()
    app.config.from_object(config_class)

    # Initialize logging
    configure_logging(app.config.get("LOG_LEVEL", "INFO"))
    logger = logging.getLogger("fintechflow.app")
    logger.info(
        "Initializing %s v%s in [%s] mode",
        app.config.get("APP_NAME"),
        app.config.get("APP_VERSION"),
        app.config.get("ENVIRONMENT"),
    )

    # Register Blueprints
    from app.routes import main_bp

    app.register_blueprint(main_bp)

    # ==============================================================================
    # Middleware: Request Timing & Metrics Observation
    # ==============================================================================

    @app.before_request
    def before_request() -> None:
        """Capture request start time for latency measurement."""
        g.start_time = time.time()

    @app.after_request
    def after_request(response: Response) -> Response:
        """Record operational metrics, response time, and apply security headers."""
        latency_ms = 0.0
        if hasattr(g, "start_time"):
            latency_ms = round((time.time() - g.start_time) * 1000, 2)

        endpoint_path = request.path
        MetricsService.record_request(endpoint_path, response.status_code)

        logger.info(
            "%s %s -> %s (%0.2f ms)",
            request.method,
            endpoint_path,
            response.status_code,
            latency_ms,
        )

        # Baseline Security Headers (Shift-Left Security Best Practices)
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["X-XSS-Protection"] = "1; mode=block"
        response.headers["Referrer-Policy"] = "strict-origin-when-cross-origin"
        response.headers["Content-Security-Policy"] = (
            "default-src 'self'; "
            "style-src 'self' 'unsafe-inline' https://fonts.googleapis.com; "
            "font-src 'self' https://fonts.gstatic.com; "
            "img-src 'self' data:;"
        )

        return response

    # ==============================================================================
    # Custom Error Handlers (JSON / HTML support)
    # ==============================================================================

    @app.errorhandler(404)
    def not_found_error(error: Any) -> tuple[Any, int]:
        """Handle 404 Not Found cleanly for API and web clients."""
        logger.warning("Resource not found: %s", request.path)
        if request.path.startswith(("/api/", "/health", "/version", "/metrics")) or (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return (
                jsonify(
                    {
                        "error": "Not Found",
                        "message": f"Endpoint '{request.path}' does not exist.",
                        "status_code": 404,
                    }
                ),
                404,
            )
        return (
            render_template(
                "404.html",
                app_name=app.config.get("APP_NAME", "FinTechFlow"),
                version=app.config.get("APP_VERSION", "1.0.0"),
                environment=app.config.get("ENVIRONMENT", "development"),
            ),
            404,
        )

    @app.errorhandler(500)
    def internal_error(error: Any) -> tuple[Any, int]:
        """Handle 500 Internal Server Error cleanly."""
        logger.error("Internal server error encountered on %s: %s", request.path, error)
        if request.path.startswith(("/api/", "/health", "/version", "/metrics")) or (
            request.accept_mimetypes.accept_json
            and not request.accept_mimetypes.accept_html
        ):
            return (
                jsonify(
                    {
                        "error": "Internal Server Error",
                        "message": "An unexpected error occurred. Please consult system logs.",
                        "status_code": 500,
                    }
                ),
                500,
            )
        return (
            render_template(
                "500.html",
                app_name=app.config.get("APP_NAME", "FinTechFlow"),
                version=app.config.get("APP_VERSION", "1.0.0"),
                environment=app.config.get("ENVIRONMENT", "development"),
            ),
            500,
        )

    return app
