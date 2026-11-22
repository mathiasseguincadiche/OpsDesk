from tests.conftest import login


def test_health_and_version(client):
    assert client.get("/health/live").json()["status"] == "alive"
    ready = client.get("/health/ready")
    assert ready.status_code == 200 and ready.json()["database"] == "up"
    assert client.get("/version").json()["application"] == "OpsDesk"


def test_metrics_exposed(client, admin):
    client.post("/api/tickets", headers=admin, json={"title": "Metric ticket"})
    body = client.get("/metrics").text
    assert "opsdesk_database_up 1.0" in body
    assert "opsdesk_http_requests_total" in body
    assert 'opsdesk_tickets{priority="normal",status="open"} 1.0' in body


def test_auth_required(client):
    assert client.get("/api/tickets").status_code == 401
    assert client.get("/api/tickets", headers={"Authorization": "Bearer nope"}).status_code == 401


def test_login_failure(client):
    r = client.post("/api/auth/login", json={"email": "admin@test.local", "password": "wrong"})
    assert r.status_code == 401


def test_register_duplicate(client, user):
    r = client.post("/api/auth/register", json={"email": "USER@test.local", "full_name": "Again", "password": "UserPass123"})
    assert r.status_code == 409


def test_ticket_lifecycle(client, user, agent):
    r = client.post("/api/tickets", headers=user, json={"title": "  VPN en panne  ", "description": "<script>x</script>", "priority": "high", "category": "network"})
    assert r.status_code == 201, r.text
    ticket = r.json()
    assert ticket["title"] == "VPN en panne" and ticket["status"] == "open"
    assert r.headers["Location"] == f"/api/tickets/{ticket['id']}"
    assert ticket["allowed_transitions"] == ["closed"]
    tid = ticket["id"]

    # requester cannot take in charge
    assert client.post(f"/api/tickets/{tid}/status", headers=user, json={"status": "in_progress"}).status_code == 403
    # agent takes it -> auto-assigned
    r = client.post(f"/api/tickets/{tid}/status", headers=agent, json={"status": "in_progress"})
    assert r.status_code == 200 and r.json()["assignee"]["full_name"] == "Agent Smith"
    # invalid jump
    assert client.post(f"/api/tickets/{tid}/status", headers=agent, json={"status": "open"}).status_code == 200
    client.post(f"/api/tickets/{tid}/status", headers=agent, json={"status": "in_progress"})
    assert client.post(f"/api/tickets/{tid}/status", headers=agent, json={"status": "closed"}).status_code == 409
    r = client.post(f"/api/tickets/{tid}/status", headers=agent, json={"status": "resolved"})
    assert r.json()["resolved_at"] is not None
    # requester comments and closes
    assert client.post(f"/api/tickets/{tid}/comments", headers=user, json={"body": "Merci !"}).status_code == 201
    r = client.post(f"/api/tickets/{tid}/status", headers=user, json={"status": "closed"})
    assert r.status_code == 200 and r.json()["status"] == "closed"
    detail = client.get(f"/api/tickets/{tid}", headers=user).json()
    assert detail["comment_count"] == 1 and detail["comments"][0]["author"]["full_name"] == "Jane User"
    kinds = [e["kind"] for e in detail["events"]]
    assert kinds[0] == "created" and "assigned" in kinds and kinds.count("status_changed") == 5
    assert detail["created_at"].endswith(("Z", "+00:00"))


def test_visibility_between_users(client, user, other_user, agent):
    tid = client.post("/api/tickets", headers=user, json={"title": "Privé"}).json()["id"]
    assert client.get(f"/api/tickets/{tid}", headers=other_user).status_code == 404
    assert client.get("/api/tickets", headers=other_user).json()["total"] == 0
    assert client.get("/api/tickets", headers=agent).json()["total"] == 1


def test_validation_errors(client, user):
    r = client.post("/api/tickets", headers=user, json={"title": "a"})
    assert r.status_code == 422 and "title" in r.json()["detail"]
    assert client.post("/api/tickets", headers=user, json={"title": "Valid", "priority": "urgent"}).status_code == 422
    assert client.post("/api/tickets", headers=user, json={"title": "Bad\x00title"}).status_code == 422
    assert client.get("/api/tickets/999999", headers=user).status_code == 404


def test_update_and_assign(client, user, agent, admin):
    tid = client.post("/api/tickets", headers=user, json={"title": "Écran noir"}).json()["id"]
    r = client.patch(f"/api/tickets/{tid}", headers=user, json={"description": "Depuis ce matin", "priority": "high"})
    assert r.status_code == 200 and r.json()["priority"] == "high"
    assert client.patch(f"/api/tickets/{tid}", headers=user, json={"assignee_id": 1}).status_code == 403
    agents = client.get("/api/users/agents", headers=agent).json()
    agent_id = next(a["id"] for a in agents if a["full_name"] == "Agent Smith")
    r = client.patch(f"/api/tickets/{tid}", headers=agent, json={"assignee_id": agent_id})
    assert r.json()["assignee"]["id"] == agent_id
    r = client.patch(f"/api/tickets/{tid}", headers=agent, json={"assignee_id": 0})
    assert r.json()["assignee"] is None
    assert client.delete(f"/api/tickets/{tid}", headers=agent).status_code == 403
    assert client.delete(f"/api/tickets/{tid}", headers=admin).status_code == 204


def test_list_filters_search_pagination(client, user, agent):
    for i in range(25):
        client.post("/api/tickets", headers=user, json={"title": f"Ticket numéro {i}", "priority": "critical" if i % 5 == 0 else "low"})
    page = client.get("/api/tickets?page=2&page_size=10", headers=agent).json()
    assert page["total"] == 25 and page["pages"] == 3 and len(page["items"]) == 10
    crit = client.get("/api/tickets?priority=critical", headers=agent).json()
    assert crit["total"] == 5
    assert client.get("/api/tickets?q=numéro 7", headers=agent).json()["total"] == 1
    first = client.get("/api/tickets?sort=priority", headers=agent).json()["items"][0]
    assert first["priority"] == "critical"
    assert client.get("/api/tickets?assignee=none", headers=agent).json()["total"] == 25


def test_stats(client, user, agent):
    tid = client.post("/api/tickets", headers=user, json={"title": "Stat", "priority": "critical"}).json()["id"]
    client.post(f"/api/tickets/{tid}/status", headers=agent, json={"status": "in_progress"})
    client.post(f"/api/tickets/{tid}/status", headers=agent, json={"status": "resolved"})
    s = client.get("/api/stats", headers=agent).json()
    assert s["total"] == 1 and s["by_status"]["resolved"] == 1
    assert len(s["timeline"]) == 14 and s["timeline"][-1]["created"] == 1 and s["timeline"][-1]["resolved"] == 1
    assert s["avg_resolution_hours"] is not None
    assert any(a["full_name"] == "Agent Smith" for a in s["agents"])


def test_user_admin(client, admin, user):
    assert client.get("/api/users", headers=user).status_code == 403
    users = client.get("/api/users", headers=admin).json()
    uid = next(u["id"] for u in users if u["email"] == "user@test.local")
    r = client.patch(f"/api/users/{uid}", headers=admin, json={"is_active": False})
    assert r.json()["is_active"] is False
    assert client.post("/api/auth/login", json={"email": "user@test.local", "password": "UserPass123"}).status_code == 403
    me = client.get("/api/auth/me", headers=admin).json()
    assert client.patch(f"/api/users/{me['id']}", headers=admin, json={"role": "user"}).status_code == 400


def test_change_password(client, user):
    assert client.put("/api/auth/me/password", headers=user, json={"current_password": "bad", "new_password": "NewPass1234"}).status_code == 400
    assert client.put("/api/auth/me/password", headers=user, json={"current_password": "UserPass123", "new_password": "NewPass1234"}).status_code == 204
    # Tous les anciens jetons deviennent invalides dès ce changement.
    assert client.get("/api/auth/me", headers=user).status_code == 401
    fresh = login(client, "user@test.local", "NewPass1234")
    assert client.get("/api/auth/me", headers=fresh).status_code == 200


def test_demo_seed(client):
    from app.bootstrap import _seed_demo
    from app.db import SessionLocal

    with SessionLocal() as db:
        _seed_demo(db)
    headers = login(client, "sophie.martin@opsdesk.local", "Demo1234!")
    stats = client.get("/api/stats", headers=headers).json()
    assert stats["total"] == 16 and stats["by_status"]["closed"] > 0

def test_browser_cookie_session_csrf_and_logout(client):
    response = client.post(
        "/api/auth/browser/login",
        json={"email": "admin@test.local", "password": "AdminPass123"},
    )
    assert response.status_code == 200, response.text
    assert "access_token" not in response.json()
    assert "httponly" in response.headers["set-cookie"].lower()
    assert client.get("/api/auth/me").status_code == 200

    # Aucun cookie ne suffit pour modifier les tickets sans en-tête CSRF.
    assert client.post("/api/tickets", json={"title": "Test CSRF protégé"}).status_code == 403
    assert client.post(
        "/api/tickets", headers={"X-CSRF-Token": "incorrect"},
        json={"title": "Test CSRF protégé"},
    ).status_code == 403
    csrf = client.cookies.get("opsdesk_csrf")
    assert csrf
    created = client.post(
        "/api/tickets", headers={"X-CSRF-Token": csrf},
        json={"title": "Test CSRF protégé"},
    )
    assert created.status_code == 201, created.text
    assert client.post("/api/auth/browser/logout").status_code == 204
    assert client.get("/api/auth/me").status_code == 401


def test_browser_cookie_session_revoked_after_password_change(client):
    response = client.post(
        "/api/auth/browser/login",
        json={"email": "admin@test.local", "password": "AdminPass123"},
    )
    assert response.status_code == 200
    csrf = client.cookies.get("opsdesk_csrf")
    assert client.put(
        "/api/auth/me/password", headers={"X-CSRF-Token": csrf},
        json={"current_password": "AdminPass123", "new_password": "AdminPass456"},
    ).status_code == 204
    assert client.get("/api/auth/me").status_code == 401
    assert client.post("/api/auth/browser/logout").status_code == 204
    assert client.post(
        "/api/auth/browser/login", json={"email": "admin@test.local", "password": "AdminPass456"}
    ).status_code == 200


def test_login_throttle_shared_by_database_and_reset_after_success(client):
    from datetime import UTC, datetime, timedelta

    from app.auth_throttle import MAX_ATTEMPTS, throttle_key
    from app.db import SessionLocal
    from app.models import LoginThrottle

    payload = {"email": "admin@test.local", "password": "incorrect"}
    for _ in range(MAX_ATTEMPTS):
        assert client.post("/api/auth/login", json=payload).status_code == 401
    limited = client.post("/api/auth/login", json=payload)
    assert limited.status_code == 429
    assert int(limited.headers["Retry-After"]) > 0
    # Même un bon mot de passe doit attendre : l'accès direct ne contourne pas le compteur.
    assert client.post(
        "/api/auth/browser/login",
        json={"email": "admin@test.local", "password": "AdminPass123"},
    ).status_code == 429

    # Une autre session SQLAlchemy voit le compteur (pas de variable locale par processus).
    with SessionLocal() as db:
        row = db.get(LoginThrottle, throttle_key("admin@test.local"))
        assert row is not None and row.attempt_count > MAX_ATTEMPTS
        row.window_started_at = datetime.now(UTC) - timedelta(minutes=10)
        row.blocked_until = datetime.now(UTC) - timedelta(seconds=1)
        db.commit()

    assert client.post(
        "/api/auth/login",
        json={"email": "admin@test.local", "password": "AdminPass123"},
    ).status_code == 200
    with SessionLocal() as db:
        assert db.get(LoginThrottle, throttle_key("admin@test.local")) is None
