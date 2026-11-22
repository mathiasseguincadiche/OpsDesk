#!/usr/bin/env python3
"""Recette native Chromium sur une pile OpsDesk Compose strictement jetable.

Le test crée un ticket fictif et ne doit jamais être exécuté sur des données réelles.
"""
from __future__ import annotations

import os
import re
from pathlib import Path

from playwright.sync_api import expect, sync_playwright

BASE = os.environ.get("OPSDESK_BASE_URL", "http://127.0.0.1:8080")
ARTIFACTS = Path("e2e-artifacts")


def main() -> None:
    ARTIFACTS.mkdir(parents=True, exist_ok=True)
    with sync_playwright() as pw:
        browser = pw.chromium.launch(headless=True)
        context = browser.new_context(viewport={"width": 1440, "height": 900}, locale="fr-FR")
        page = context.new_page()
        try:
            page.goto(BASE, wait_until="domcontentloaded")
            expect(page.get_by_role("heading", name="Connexion à votre espace")).to_be_visible(timeout=20000)
            page.get_by_label("Adresse e-mail professionnelle").fill("sophie.martin@opsdesk.local")
            page.get_by_label("Mot de passe").fill("Demo1234!")
            page.get_by_role("button", name="Se connecter").click()
            expect(page.get_by_role("button", name="Menu du compte")).to_be_visible(timeout=20000)

            cookies = {cookie["name"]: cookie for cookie in context.cookies()}
            session = cookies["opsdesk_session"]
            csrf = cookies["opsdesk_csrf"]
            assert session["httpOnly"] and session["sameSite"] == "Strict"
            assert not csrf["httpOnly"] and csrf["sameSite"] == "Strict"
            assert page.evaluate("window.localStorage.getItem('opsdesk-token')") is None

            # Un appel direct par le navigateur, sans jeton CSRF, doit être refusé.
            status = page.evaluate("""async () => {
                const r = await fetch('/api/tickets', {
                    method: 'POST',
                    headers: {'Content-Type': 'application/json'},
                    body: JSON.stringify({title: 'CSRF refusé par E2E'})
                });
                return r.status;
            }""")
            assert status == 403, f"Mutation sans CSRF non rejetée : HTTP {status}"

            page.get_by_role("button", name="Nouveau ticket").first.click()
            subject = "Recette Chromium — ticket fictif"
            page.get_by_label("Sujet").fill(subject)
            page.get_by_role("button", name="Créer le ticket").click()
            expect(page).to_have_url(re.compile(r"/tickets/\d+"), timeout=20000)
            expect(page.get_by_role("heading", name=subject)).to_be_visible(timeout=20000)
            page.screenshot(path=str(ARTIFACTS / "bureau-ticket.png"), full_page=True)

            page.reload(wait_until="domcontentloaded")
            expect(page.get_by_role("heading", name=subject)).to_be_visible(timeout=20000)

            page.get_by_role("button", name="Menu du compte").click()
            page.get_by_role("button", name="Se déconnecter").click()
            expect(page.get_by_role("heading", name="Connexion à votre espace")).to_be_visible(timeout=20000)
            page.wait_for_function("!document.cookie.includes('opsdesk_csrf=')", timeout=10000)
            page.reload(wait_until="domcontentloaded")
            expect(page.get_by_role("heading", name="Connexion à votre espace")).to_be_visible(timeout=20000)

            mobile = browser.new_context(viewport={"width": 390, "height": 844}, is_mobile=True, has_touch=True)
            try:
                mp = mobile.new_page()
                mp.goto(BASE, wait_until="domcontentloaded")
                expect(mp.get_by_role("heading", name="Connexion à votre espace")).to_be_visible(timeout=20000)
                width = mp.evaluate("document.documentElement.scrollWidth")
                assert width <= 392, f"Débordement horizontal mobile : {width}px"
                mp.screenshot(path=str(ARTIFACTS / "mobile-connexion.png"), full_page=True)
            finally:
                mobile.close()

            print("PASS : Chromium — cookies HttpOnly, CSRF, ticket, rechargement, déconnexion, mobile.")
        except Exception:
            page.screenshot(path=str(ARTIFACTS / "echec.png"), full_page=True)
            raise
        finally:
            context.close()
            browser.close()


if __name__ == "__main__":
    main()
