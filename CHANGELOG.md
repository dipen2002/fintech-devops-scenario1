# Changelog

All notable changes to the **FinTechFlow** project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [1.1.0] - 2026-08-29

### Added
- Blue-Green release candidate demonstration deployment slot (`docker-compose.bluegreen.yml`).
- Active operational metrics endpoint (`GET /metrics`) with request and error rate tracking.
- Category filtering capabilities on simulated transaction API (`GET /api/transactions?category=Utilities`).
- Comprehensive DevSecOps documentation suite in `docs/`.

### Changed
- Refactored health checks to utilize Python standard library probes without external curl dependencies.
- Standardized environment-specific configuration loaders for development, staging, and production.

### Security
- Upgraded production dependencies to latest patched releases with zero known CVEs (`pip-audit` verified).
- Added Content Security Policy and anti-sniffing HTTP headers to all Flask endpoints.

---

## [1.0.0] - 2026-08-28

### Added
- Initial release of the **FinTechFlow** educational DevOps demonstration platform.
- Flask application core with modern responsive fintech dashboard.
- Synthetic mock domain services: `AccountService` and `TransactionService`.
- Automated health check endpoint (`GET /health`) and version endpoint (`GET /version`).
- 10-stage continuous integration workflow in `.github/workflows/ci.yml`.
- Pytest automated test suite covering unit tests, API tests, and 404 error handlers.
- Code quality and style enforcement with Ruff (`ruff check .`).
- Static application security testing (SAST) with Bandit (`bandit -r app`).
- Software composition analysis (SCA) with `pip-audit`.
- Multi-stage production `Dockerfile` with non-root execution (`appuser:10001`).
- Local container orchestration with `docker-compose.yml`.
- Infrastructure as Code (IaC) configuration using Terraform (`terraform/`).
- Initial architecture, rollback, and environment documentation.
