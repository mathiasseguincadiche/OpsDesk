"""Garde-fous de configuration, sans accès à la base de données."""
import pytest

from app.config import Settings, _validate_production_settings


@pytest.fixture
def production_settings(monkeypatch):
    for name, value in {
        "JWT_SECRET": "unit-test-jwt-key-of-sufficient-length",
        "ADMIN_PASSWORD": "unit-test-admin-password",
        "DB_PASSWORD": "unit-test-db-password",
    }.items():
        monkeypatch.delenv(f"{name}_FILE", raising=False)
        monkeypatch.setenv(name, value)
    return Settings(environment="production", database_url=None, seed_demo_data=False)


@pytest.mark.parametrize("name", ["JWT_SECRET", "ADMIN_PASSWORD", "DB_PASSWORD"])
def test_missing_secret(monkeypatch, production_settings, name):
    monkeypatch.delenv(name)
    with pytest.raises(RuntimeError, match=name):
        _validate_production_settings(production_settings)


@pytest.mark.parametrize("name", ["JWT_SECRET", "ADMIN_PASSWORD", "DB_PASSWORD"])
def test_placeholder_secret(monkeypatch, production_settings, name):
    monkeypatch.setenv(name, "change-me-not-a-real-secret-long-enough")
    with pytest.raises(RuntimeError, match=name):
        _validate_production_settings(production_settings)


def test_distinct_secrets(monkeypatch, production_settings):
    monkeypatch.setenv("DB_PASSWORD", "unit-test-admin-password")
    with pytest.raises(RuntimeError, match="distincts"):
        _validate_production_settings(production_settings)


def test_file_precedence(monkeypatch, production_settings, tmp_path):
    secret = tmp_path / "admin"
    secret.write_text("unit-test-admin-file-password", encoding="utf-8")
    monkeypatch.setenv("ADMIN_PASSWORD_FILE", str(secret))
    monkeypatch.setenv("ADMIN_PASSWORD", "change-me")
    _validate_production_settings(production_settings)


def test_valid_secrets(production_settings):
    _validate_production_settings(production_settings)


def test_demo_data_forbidden_in_production(production_settings):
    production_settings.seed_demo_data = True
    with pytest.raises(RuntimeError, match="SEED_DEMO_DATA"):
        _validate_production_settings(production_settings)


def test_demo_data_disabled_allows_other_production_checks(production_settings):
    assert production_settings.seed_demo_data is False
    _validate_production_settings(production_settings)
