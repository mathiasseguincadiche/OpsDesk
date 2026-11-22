#!/usr/bin/env python3
"""Vérifier la limitation des rafales de connexions via nginx, sur un socle jetable.

Le script envoie volontairement des connexions invalides. Ne pas exécuter
sur une instance partagée : il peut temporairement bloquer cette IP.
"""
from __future__ import annotations

import json
import sys
import urllib.error
import urllib.request

BASE = (sys.argv[1] if len(sys.argv) > 1 else "http://127.0.0.1:8080").rstrip("/")
payload = json.dumps({"email": "inconnu@opsdesk.local", "password": "incorrect"}).encode("utf-8")
codes: list[int] = []

for _ in range(26):
    request = urllib.request.Request(
        f"{BASE}/api/auth/login", data=payload,
        headers={"Content-Type": "application/json"}, method="POST",
    )
    try:
        with urllib.request.urlopen(request, timeout=10) as response:
            code = response.status
    except urllib.error.HTTPError as error:
        code = error.code
    codes.append(code)
    if code not in (401, 429):
        raise SystemExit(f"Code inattendu sur la connexion invalide : {code}")

if 429 not in codes:
    raise SystemExit(f"Limitation absente : 429 non observé dans {len(codes)} tentatives.")

with urllib.request.urlopen(f"{BASE}/healthz", timeout=5) as response:
    if response.status != 200:
        raise SystemExit("La limitation d'authentification affecte une sonde publique.")

print(f"Limitation nginx vérifiée : {codes.count(429)} refus HTTP 429 sur {len(codes)} tentatives.")
