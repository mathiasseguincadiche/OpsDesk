#!/usr/bin/env python3
"""Smoke test HTTP de bout en bout, à travers le frontend nginx.

Usage : python3 scripts/smoke.py [http://127.0.0.1:8080]
Nécessite les données de démo (SEED_DEMO_DATA=true). Code retour non nul en cas d'échec.
"""
import json
import sys
import urllib.error
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080").rstrip("/")
def call(path, method="GET", body=None, token=None, expect=200):
    req = urllib.request.Request(BASE + path, method=method, data=json.dumps(body).encode() if body is not None else None)
    if body is not None: req.add_header("Content-Type", "application/json")
    if token: req.add_header("Authorization", "Bearer " + token)
    try: r = urllib.request.urlopen(req, timeout=10)
    except urllib.error.HTTPError as e: r = e
    data = r.read().decode()
    assert r.status == expect, (path, r.status, data[:200])
    print(f"OK {method:6} {path:40} {r.status}")
    return (json.loads(data) if data and r.headers.get("Content-Type","").startswith("application/json") else data), r.headers
call("/health/ready"); call("/version")
html, h = call("/"); assert "<div id=\"root\">" in html; print("   CSP:", h["Content-Security-Policy"][:90], "...")
call("/tickets/3")  # SPA fallback
call("/metrics", expect=404)
call("/api/tickets", expect=401)
agent = call("/api/auth/login", "POST", {"email": "sophie.martin@opsdesk.local", "password": "Demo1234!"})[0]["access_token"]
user = call("/api/auth/login", "POST", {"email": "julie.durand@opsdesk.local", "password": "Demo1234!"})[0]["access_token"]
page = call("/api/tickets?page_size=5", token=agent)[0]; print("   total tickets:", page["total"])
t = call("/api/tickets", "POST", {"title": "Smoke test — accents éàü", "priority": "high", "category": "network"}, token=user, expect=201)[0]
call(f"/api/tickets/{t['id']}/status", "POST", {"status": "in_progress"}, token=agent)
call(f"/api/tickets/{t['id']}/comments", "POST", {"body": "On regarde"}, token=agent, expect=201)
call(f"/api/tickets/{t['id']}/status", "POST", {"status": "resolved"}, token=agent)
d = call(f"/api/tickets/{t['id']}/status", "POST", {"status": "closed"}, token=user)[0]; assert d["status"] == "closed"
s = call("/api/stats", token=agent)[0]; print("   stats:", s["by_status"], "avg h:", s["avg_resolution_hours"])
call("/api/docs")
print("ALL GOOD")
