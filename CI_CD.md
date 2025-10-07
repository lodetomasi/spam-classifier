# CI/CD Pipeline Documentation

This project includes comprehensive CI/CD pipelines for automated testing, quality assurance, and deployment.

## Overview

```
┌─────────────────┐
│   Code Push     │
└────────┬────────┘
         │
    ┌────▼────┐
    │   CI    │ ──► Validate, Test, Lint, Security Scan
    └────┬────┘
         │
    ┌────▼────┐
    │ Quality │ ──► Code Complexity, Agent Validation
    └────┬────┘
         │
    ┌────▼────┐
    │   CD    │ ──► Release, Package, Deploy
    └─────────┘
```

## GitHub Actions Workflows

### 1. CI - Continuous Integration (`.github/workflows/ci.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main` or `develop`

**Jobs:**

#### Validate
- ✅ Project structure verification
- ✅ Required files check
- ✅ Agent configurations validation
- ✅ Data files validation

#### Lint
- ✅ flake8 (syntax errors, undefined names)
- ✅ black (code formatting)
- ✅ isort (import sorting)
- ✅ pylint (code quality)

#### Test
- ✅ Python syntax validation
- ✅ Pattern catalog loading test
- ✅ Script execution validation

#### Security
- ✅ safety (dependency vulnerabilities)
- ✅ bandit (security issues)
- ✅ Security report artifacts

#### Documentation
- ✅ README completeness
- ✅ Specification validation
- ✅ Results documentation check

**Status Badge:**
```markdown
![CI](https://github.com/lodetomasi/spam-classifier/workflows/CI%20-%20Continuous%20Integration/badge.svg)
```

---

### 2. CD - Continuous Delivery (`.github/workflows/cd.yml`)

**Triggers:**
- Tag push matching `v*.*.*` (e.g., `v1.0.0`)
- Manual workflow dispatch

**Jobs:**

#### Create Release
1. Extract version from tag
2. Generate changelog from git commits
3. Create release archives (`.tar.gz`, `.zip`)
4. Publish GitHub release
5. Attach release artifacts

**Creating a Release:**
```bash
# Tag the release
git tag -a v1.0.0 -m "Release version 1.0.0"
git push origin v1.0.0

# Or manual trigger via GitHub UI:
# Actions → CD - Continuous Delivery → Run workflow
```

#### Publish Docs
- Builds documentation site with mkdocs
- Deploys to GitHub Pages (if configured)

#### Docker Build (Optional)
- Builds Docker image
- Pushes to GitHub Container Registry
- Tags: `latest` and version tag

**Status Badge:**
```markdown
![CD](https://github.com/lodetomasi/spam-classifier/workflows/CD%20-%20Continuous%20Delivery/badge.svg)
```

---

### 3. Code Quality (`.github/workflows/quality.yml`)

**Triggers:**
- Push to `main` or `develop`
- Pull requests to `main`
- Weekly schedule (Sunday 00:00 UTC)

**Jobs:**

#### Code Quality Analysis
- Code complexity (radon, mccabe)
- Cyclomatic complexity check
- Pylint analysis
- Quality reports artifacts

#### Agent Validation
- Markdown syntax validation
- Frontmatter completeness
- Agent prompt quality checks

#### Pattern Catalog Validation
- JSON structure validation
- Required keys verification
- Pattern count reporting

#### Documentation Quality
- Section completeness
- Broken link detection
- Specification validation

---

### 4. Test Real Agents (`.github/workflows/test-agents.yml`)

**Triggers:**
- Manual workflow dispatch only

**Purpose:**
Prepares test environment for real agent testing (requires manual execution with Claude Code).

**Usage:**
```bash
# 1. Trigger workflow
Actions → Test Real Agents → Run workflow → Select email count

# 2. Run locally
python src/batch_test.py

# 3. Invoke agents via Claude Code Task tool

# 4. Save results
results/test_results_YYYYMMDD_HHMMSS.json

# 5. Calculate metrics
python src/batch_test.py --calculate results/test_results_*.json
```

---

## Docker Support

### Build Docker Image

```bash
docker build -t spam-classifier:latest .
```

### Run Container

```bash
# Basic run
docker run spam-classifier:latest

# With volume mounting for results
docker run -v $(pwd)/results:/app/results spam-classifier:latest

# Interactive mode
docker run -it spam-classifier:latest /bin/bash
```

### Docker Compose (Optional)

Create `docker-compose.yml`:
```yaml
version: '3.8'
services:
  spam-classifier:
    build: .
    volumes:
      - ./results:/app/results
    environment:
      - PYTHONUNBUFFERED=1
```

Run with:
```bash
docker-compose up
```

---

## GitHub Templates

### Pull Request Template

When creating a PR, the template includes:
- Change type selection
- Agent testing checklist
- Performance impact assessment
- Documentation requirements

**Location:** `.github/PULL_REQUEST_TEMPLATE.md`

### Issue Templates

#### Bug Report
- Detailed reproduction steps
- Email sample section
- Agent response logging
- Environment information

**Location:** `.github/ISSUE_TEMPLATE/bug_report.md`

#### Feature Request
- Problem statement
- Proposed solution
- Agent impact assessment
- Implementation complexity

**Location:** `.github/ISSUE_TEMPLATE/feature_request.md`

---

## Local Development Workflow

### 1. Before Committing

```bash
# Run linters
flake8 src/
black --check src/
isort --check src/

# Format code
black src/
isort src/

# Run local tests
python src/batch_test.py

# Validate pattern catalog
python -c "import json; json.load(open('data/pattern_catalog.json'))"
```

### 2. Commit Guidelines

```bash
# Conventional commits
git commit -m "feat: add new spam pattern detection"
git commit -m "fix: correct intent analyzer scoring"
git commit -m "docs: update README with examples"
git commit -m "test: add pharmaceutical spam tests"
git commit -m "ci: update CI workflow timeout"
```

### 3. Creating a Release

```bash
# 1. Update version in relevant files
# 2. Update CHANGELOG.md
# 3. Commit changes
git add .
git commit -m "chore: prepare release v1.1.0"

# 4. Create tag
git tag -a v1.1.0 -m "Release v1.1.0 - Improved pattern recognition"

# 5. Push
git push origin main
git push origin v1.1.0
```

The CD pipeline will automatically:
- Create release archives
- Generate changelog
- Publish GitHub release
- Build Docker image

---

## Monitoring and Artifacts

### CI Pipeline Artifacts

**Security Reports:**
- `bandit-report.json` - Security scan results
- Available in workflow run artifacts

**Quality Reports:**
- `complexity-report.txt` - Code complexity analysis
- `pylint-report.json` - Pylint analysis
- Available in workflow run artifacts

### Viewing Workflow Status

1. Navigate to GitHub Actions tab
2. Select workflow run
3. View job summaries and logs
4. Download artifacts if available

### Status Badges

Add to README:
```markdown
![CI](https://github.com/lodetomasi/spam-classifier/workflows/CI%20-%20Continuous%20Integration/badge.svg)
![CD](https://github.com/lodetomasi/spam-classifier/workflows/CD%20-%20Continuous%20Delivery/badge.svg)
![Quality](https://github.com/lodetomasi/spam-classifier/workflows/Code%20Quality%20&%20Coverage/badge.svg)
```

---

## Troubleshooting

### CI Failures

**Linting Errors:**
```bash
# Fix locally
black src/
isort src/
flake8 src/ --exit-zero
```

**Security Issues:**
```bash
# Check dependencies
safety check --file requirements.txt

# Update vulnerable packages
pip install --upgrade <package>
```

**Test Failures:**
```bash
# Run tests locally
python src/batch_test.py
python -m pytest tests/
```

### CD Failures

**Tag Issues:**
```bash
# Delete and recreate tag
git tag -d v1.0.0
git push origin :refs/tags/v1.0.0
git tag -a v1.0.0 -m "Release v1.0.0"
git push origin v1.0.0
```

**Release Artifacts:**
- Check workflow logs
- Verify file permissions
- Ensure required files exist

---

## Best Practices

### 1. Branch Protection

Configure in GitHub Settings → Branches:
- ✅ Require pull request reviews
- ✅ Require status checks (CI, Quality)
- ✅ Require linear history
- ✅ Include administrators

### 2. Secrets Management

For private deployments:
```bash
# Add secrets in GitHub Settings → Secrets
DOCKER_USERNAME
DOCKER_TOKEN
DEPLOY_KEY
```

### 3. Workflow Optimization

**Cache Dependencies:**
```yaml
- uses: actions/cache@v3
  with:
    path: ~/.cache/pip
    key: ${{ runner.os }}-pip-${{ hashFiles('requirements.txt') }}
```

**Matrix Testing:**
```yaml
strategy:
  matrix:
    python-version: ['3.9', '3.10', '3.11']
```

---

## Future Enhancements

### Planned

- [ ] Automated performance benchmarking
- [ ] Integration with Claude API for automated agent testing
- [ ] Deployment to cloud platforms (AWS, GCP, Azure)
- [ ] Slack/Discord notifications for releases
- [ ] Code coverage reporting with codecov
- [ ] Automated dependency updates (Dependabot)

### Configuration

See individual workflow files for detailed configuration options.

---

**Last Updated:** 2025-10-07
**Version:** 2.0
**Status:** ✅ Production Ready
