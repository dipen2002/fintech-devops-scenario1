"""Configuration management for FinTechFlow application.

Provides distinct configuration profiles for development, testing,
staging, and production environments using environment variables.
"""

import os


class Config:
    """Base configuration with safe defaults."""

    APP_NAME: str = os.getenv("APP_NAME", "FinTechFlow")
    APP_VERSION: str = os.getenv("APP_VERSION", "1.0.0")
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development").lower()

    # Secret key - fallback is only acceptable in dev/test, production must enforce env var
    SECRET_KEY: str = os.getenv(
        "SECRET_KEY", "dev-fallback-insecure-secret-key-educational-only"
    )

    # Server settings
    PORT: int = int(os.getenv("PORT", "5000"))
    HOST: str = os.getenv("HOST", "0.0.0.0")  # nosec B104

    # Logging
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO").upper()

    # Feature flags & observability
    ENABLE_METRICS: bool = True
    TESTING: bool = False
    DEBUG: bool = False


class DevelopmentConfig(Config):
    """Configuration for local developer workstations."""

    DEBUG: bool = True
    LOG_LEVEL: str = "DEBUG"
    ENVIRONMENT: str = "development"


class TestingConfig(Config):
    """Configuration for automated test execution in CI/CD."""

    TESTING: bool = True
    DEBUG: bool = False
    LOG_LEVEL: str = "WARNING"
    ENVIRONMENT: str = "testing"
    SECRET_KEY: str = "test-only-secret-key-for-unit-tests"


class StagingConfig(Config):
    """Configuration for pre-production release validation environment."""

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "staging"


class ProductionConfig(Config):
    """Configuration for live production environment."""

    DEBUG: bool = False
    LOG_LEVEL: str = "INFO"
    ENVIRONMENT: str = "production"


_CONFIG_MAPPING: dict[str, type[Config]] = {
    "development": DevelopmentConfig,
    "dev": DevelopmentConfig,
    "testing": TestingConfig,
    "test": TestingConfig,
    "staging": StagingConfig,
    "stage": StagingConfig,
    "production": ProductionConfig,
    "prod": ProductionConfig,
}


def get_config(env_name: str | None = None) -> type[Config]:
    """Retrieve configuration class based on environment name."""
    if env_name is None:
        env_name = os.getenv("ENVIRONMENT", "development")
    return _CONFIG_MAPPING.get(env_name.lower(), DevelopmentConfig)
