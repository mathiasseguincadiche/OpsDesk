"""Initialiser le schéma, le premier administrateur et les données fictives éventuelles.

L'initialisation est répétable. Sous PostgreSQL, un verrou consultatif protège
les démarrages simultanés de plusieurs instances.
"""
from __future__ import annotations

import logging
import random
from contextlib import contextmanager
from datetime import timedelta

from sqlalchemy import func, select, text

from .config import get_settings
from .db import Base, SessionLocal, engine
from .models import Comment, Ticket, TicketEvent, User, utcnow
from .security import hash_password

log = logging.getLogger("opsdesk.bootstrap")
_LOCK_ID = 727_001

DEMO_PASSWORD = "Demo1234!"
DEMO_USERS = [
    ("sophie.martin@opsdesk.local", "Sophie Martin", "agent"),
    ("karim.benali@opsdesk.local", "Karim Benali", "agent"),
    ("julie.durand@opsdesk.local", "Julie Durand", "user"),
    ("thomas.petit@opsdesk.local", "Thomas Petit", "user"),
    ("lea.moreau@opsdesk.local", "Léa Moreau", "user"),
]
DEMO_TICKETS = [
    ("Imprimante du 2e étage hors ligne", "L'imprimante HP du couloir B n'apparaît plus sur le réseau depuis ce matin.", "hardware", "normal"),
    ("Accès VPN impossible depuis le domicile", "Erreur « authentication failed » avec le client VPN, alors que mon mot de passe fonctionne sur la messagerie.", "access", "high"),
    ("Création d'un compte pour un nouvel arrivant", "Arrivée de Marc Lefèvre lundi prochain au service comptabilité : compte AD, messagerie et accès ERP.", "access", "normal"),
    ("Le Wi-Fi invité coupe toutes les 10 minutes", "Les visiteurs de la salle de réunion Everest perdent la connexion régulièrement.", "network", "high"),
    ("Mise à jour de la suite bureautique", "Demande d'installation de la dernière version sur mon poste.", "software", "low"),
    ("Serveur de fichiers très lent", "Ouvrir un document sur le partage \\\\files\\projets prend plus d'une minute.", "network", "critical"),
    ("Écran secondaire qui clignote", "Le second écran clignote dès que je branche l'ordinateur sur la station d'accueil.", "hardware", "low"),
    ("Licence logicielle expirée", "Le logiciel de DAO affiche « licence expirée » au démarrage.", "software", "high"),
    ("Réinitialisation du mot de passe ERP", "Compte verrouillé après trop de tentatives.", "access", "normal"),
    ("Messagerie : pièces jointes bloquées", "Impossible d'envoyer des fichiers .zip à un client.", "software", "normal"),
    ("Téléphone IP sans tonalité", "Poste 4521, plus de tonalité depuis le déménagement du bureau.", "hardware", "normal"),
    ("Panne réseau salle serveurs B", "Alerte de supervision : switch de la baie 3 injoignable.", "network", "critical"),
    ("Demande de second écran", "Pour le travail sur les tableaux de bord, un second écran serait utile.", "hardware", "low"),
    ("Certificat TLS de l'intranet expiré", "Le navigateur affiche un avertissement de sécurité sur l'intranet.", "software", "high"),
    ("Accès au dossier partagé RH", "Besoin d'un accès en lecture au dossier RH/Formation.", "access", "low"),
    ("Sauvegarde nocturne en échec", "Le job de sauvegarde de la base comptable échoue depuis deux nuits.", "other", "critical"),
]
DEMO_COMMENTS = [
    "Merci pour votre signalement, nous regardons cela.",
    "Pouvez-vous redémarrer le poste et nous dire si le problème persiste ?",
    "C'est fait, le problème est toujours présent.",
    "Intervention planifiée cet après-midi.",
    "Correctif appliqué, pouvez-vous confirmer ?",
]


@contextmanager
def _init_lock():
    if engine.dialect.name != "postgresql":
        yield
        return
    with engine.connect() as conn:
        conn.execute(text("SELECT pg_advisory_lock(:id)"), {"id": _LOCK_ID})
        try:
            yield
        finally:
            conn.execute(text("SELECT pg_advisory_unlock(:id)"), {"id": _LOCK_ID})
            conn.commit()


def init_database() -> None:
    settings = get_settings()
    # Ne jamais créer de comptes à mot de passe public sur une cible de production.
    if settings.environment == "production" and settings.seed_demo_data:
        raise RuntimeError("SEED_DEMO_DATA doit être désactivé (false) en production.")
    with _init_lock():
        Base.metadata.create_all(engine)
        with SessionLocal() as db:
            if not db.scalar(select(func.count()).select_from(User).where(User.role == "admin")):
                db.add(
                    User(
                        email=settings.admin_email.lower(),
                        full_name=settings.admin_name,
                        password_hash=hash_password(settings.admin_password),
                        role="admin",
                    )
                )
                db.commit()
                log.info("admin_created email=%s", settings.admin_email)
            if settings.seed_demo_data and not db.scalar(select(func.count()).select_from(Ticket)):
                _seed_demo(db)


def _seed_demo(db) -> None:
    rng = random.Random(42)
    password_hash = hash_password(DEMO_PASSWORD)
    users = []
    for email, name, role in DEMO_USERS:
        user = db.scalar(select(User).where(User.email == email))
        if user is None:
            user = User(email=email, full_name=name, role=role, password_hash=password_hash)
            db.add(user)
        users.append(user)
    db.flush()
    agents = [u for u in users if u.role == "agent"]
    requesters = [u for u in users if u.role == "user"]
    now = utcnow()

    for index, (title, description, category, priority) in enumerate(DEMO_TICKETS):
        created = now - timedelta(days=rng.randint(0, 13), hours=rng.randint(0, 20), minutes=rng.randint(0, 59))
        requester = requesters[index % len(requesters)]
        status = ["open", "in_progress", "resolved", "closed"][index % 4] if index > 2 else "open"
        ticket = Ticket(
            title=title, description=description, category=category, priority=priority,
            requester_id=requester.id, status="open", created_at=created, updated_at=created,
        )
        db.add(ticket)
        db.flush()
        db.add(TicketEvent(ticket_id=ticket.id, actor_id=requester.id, kind="created", to_value="open", created_at=created))
        moment = created
        if status != "open":
            agent = agents[index % len(agents)]
            moment += timedelta(hours=rng.randint(1, 6))
            ticket.assignee_id = agent.id
            ticket.status = "in_progress"
            db.add(TicketEvent(ticket_id=ticket.id, actor_id=agent.id, kind="assigned", to_value=agent.full_name, created_at=moment))
            db.add(TicketEvent(ticket_id=ticket.id, actor_id=agent.id, kind="status_changed", from_value="open", to_value="in_progress", created_at=moment))
            for offset, body in enumerate(DEMO_COMMENTS[: rng.randint(1, 4)]):
                author = agent if offset % 2 == 0 else requester
                db.add(Comment(ticket_id=ticket.id, author_id=author.id, body=body, created_at=moment + timedelta(minutes=30 * (offset + 1))))
            if status in ("resolved", "closed"):
                moment = min(now, moment + timedelta(hours=rng.randint(2, 40)))
                ticket.status = "resolved"
                ticket.resolved_at = moment
                db.add(TicketEvent(ticket_id=ticket.id, actor_id=agent.id, kind="status_changed", from_value="in_progress", to_value="resolved", created_at=moment))
            if status == "closed":
                moment = min(now, moment + timedelta(hours=rng.randint(1, 12)))
                ticket.status = "closed"
                ticket.closed_at = moment
                db.add(TicketEvent(ticket_id=ticket.id, actor_id=requester.id, kind="status_changed", from_value="resolved", to_value="closed", created_at=moment))
        ticket.updated_at = moment
    db.commit()
    log.info("demo_data_seeded tickets=%s users=%s", len(DEMO_TICKETS), len(DEMO_USERS))
