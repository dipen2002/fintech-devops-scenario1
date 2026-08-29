# FinTechFlow – CI/CD Pipeline & Delivery Lifecycle

## 1. CI/CD Strategy Overview

In **Scenario 1**, the company operated with:
- Long 12-week release cycles resulting in massive changesets.
- Manual deployment scripts executed across dozens of servers by 30 engineers over weekends.
- Uncoordinated testing leading to repeated production failures and rollbacks.

The **FinTechFlow CI/CD Strategy** introduces automated quality gates, automated testing, container builds, and pre-deployment smoke checks.

---

## 2. Complete Delivery Lifecycle Flow

```mermaid
flowchart TD
    subgraph DevelopmentCycle ["1. Continuous Integration (Shift-Left)"]
        Dev["Developer creates Feature Branch"] --> Commit["Local Commits & Pre-commit Checks"]
        Commit --> PR["Submit Pull Request to 'main'"]
        PR --> GHA["GitHub Actions CI Workflow Triggered"]
        
        subgraph PipelineGates ["10-Stage Automated Quality Gate"]
            S1["Stage 1: Checkout Repository"] --> S2["Stage 2: Setup Python 3.12 Runtime"]
            S2 --> S3["Stage 3: Install Dependencies"]
            S3 --> S4["Stage 4: Linting (Ruff Check)"]
            S4 --> S5["Stage 5: Test Execution (Pytest)"]
            S5 --> S6["Stage 6: Coverage Gate (>80%)"]
            S6 --> S7["Stage 7: SAST Security Scan (Bandit)"]
            S7 --> S8["Stage 8: SCA Dependency Audit (pip-audit)"]
            S8 --> S9["Stage 9: Container Image Build (Docker)"]
            S9 --> S10["Stage 10: CI Gate Validation"]
        end
    end

    subgraph StagingPhase ["2. Continuous Delivery to Staging"]
        S10 --> Merge["Pull Request Approved & Merged to 'main'"]
        Merge --> DeployStaging["Automated Deploy to Staging (Slot Green)"]
        DeployStaging --> SmokeTest["Automated Smoke Test: GET /health & /version"]
    end

    subgraph ProductionPhase ["3. Production Blue-Green Cutover"]
        SmokeTest -->|"Staging Validated"| BlueGreenCutover["Traffic Router Switched to Green Slot"]
        BlueGreenCutover --> MonitorProd["Monitor /metrics & Log Stream"]
        MonitorProd -->|"Anomalies Detected"| FastRollback["Instant Rollback to Blue Slot"]
        MonitorProd -->|"Healthy"| ReleaseComplete["Release Complete & Tagged (v1.1.0)"]
    end
```

---

## 3. GitHub Actions CI Pipeline Stages Explained

The CI workflow (`.github/workflows/ci.yml`) executes automatically on every `push` and `pull_request` against the `main` branch.

| Stage | Action / Tool | Purpose & Scenario 1 Problem Solved | Pass Criteria |
| :--- | :--- | :--- | :--- |
| **Stage 1: Checkout** | `actions/checkout@v4` | Pulls repository codebase with complete commit history. | Git repository cloned cleanly. |
| **Stage 2: Setup Python** | `actions/setup-python@v5` | Provisions Python 3.12 execution environment with pip caching. | Python runtime initialized. |
| **Stage 3: Dependencies** | `pip install` | Installs pinned runtime and test packages from `requirements-dev.txt`. | Zero package installation errors. |
| **Stage 4: Code Quality** | `ruff check .` | Enforces code formatting, PEP 8 rules, unused import cleanup, and Python modernizations. | Zero linting errors or warnings. |
| **Stage 5: Test Execution** | `pytest -q` | Executes 18 unit, API, configuration, and integration tests. | 100% test pass rate. |
| **Stage 6: Code Coverage** | `pytest-cov` | Generates coverage metrics and enforces test coverage threshold (>80%). | App coverage > 80% (Current: 97%). |
| **Stage 7: SAST Scan** | `bandit -r app` | Performs Static Application Security Testing on AST for security flaws. | Zero high/medium security issues. |
| **Stage 8: SCA Audit** | `pip-audit` | Audits third-party dependencies against PyPA vulnerability database. | Zero known vulnerable packages. |
| **Stage 9: Docker Build** | `docker build` | Builds immutable container image with multi-stage non-root containerfile. | Docker image successfully builds. |
| **Stage 10: CI Gate** | Shell summary | Synthesizes stage outcomes and authorizes progression to staging deployment. | All previous 9 stages green. |

---

## 4. Pipeline Execution Commands (Local Replication)

To reproduce the exact CI pipeline checks on a local workstation before submitting a Pull Request:

```bash
# Activate virtual environment
source .venv/bin/activate  # (Linux/macOS)
.\.venv\Scripts\Activate.ps1 # (Windows PowerShell)

# Step 1: Linting
ruff check .

# Step 2: Automated Tests & Coverage
pytest -q
pytest --cov=app --cov-report=term-missing

# Step 3: Security Scans
bandit -r app
pip-audit

# Step 4: Docker Container Build
docker build -t fintechflow:local .
```

---

## 5. Pull Request Quality Gate Rules

In a production GitHub repository, branch protection rules on `main` ensure:
1. **Require Status Checks to Pass**: `Continuous Integration & Quality Gates` must be green before merging.
2. **Require Code Review**: At least 1 peer approval required.
3. **No Direct Pushes**: All changes must arrive via pull request branches.
4. **Up-to-date Branches**: Branch must be rebased or merged with latest `main` before merge.
