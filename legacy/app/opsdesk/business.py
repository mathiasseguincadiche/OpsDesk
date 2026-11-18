"""Small, explicit ticket rules; independent of HTTP and PostgreSQL."""
STATUSES = ("open", "in_progress", "closed")
PRIORITIES = ("low", "normal", "high")


class InvalidTicket(ValueError):
    pass


def ticket_input(payload):
    if not isinstance(payload, dict):
        raise InvalidTicket("Un objet titre/description/priorité est attendu.")
    values = {}
    for key, default, minimum, maximum in [
        ("title", "", 3, 120), ("description", "", 0, 2000)
    ]:
        value = payload.get(key, default)
        if not isinstance(value, str):
            raise InvalidTicket(f"{key} doit être un texte.")
        # PostgreSQL text cannot store NUL or invalid UTF-8 surrogate code points.
        # Reject malformed input as 400 instead of misreporting a DB outage/500.
        try:
            value.encode("utf-8")
        except UnicodeEncodeError as error:
            raise InvalidTicket(f"{key} doit être un texte Unicode valide.") from error
        if "\x00" in value:
            raise InvalidTicket(f"{key} ne doit pas contenir de caractère NUL.")
        value = value.strip()
        if not minimum <= len(value) <= maximum:
            raise InvalidTicket(f"{key} doit contenir de {minimum} à {maximum} caractères.")
        values[key] = value
    priority = payload.get("priority", "normal")
    if not isinstance(priority, str) or priority not in PRIORITIES:
        raise InvalidTicket("La priorité doit être low, normal ou high.")
    values["priority"] = priority
    return values


def next_status(current, target):
    if not isinstance(target, str) or target not in STATUSES:
        raise InvalidTicket("Le statut doit être open, in_progress ou closed.")
    transitions = {"open": {"open", "in_progress"}, "in_progress": {"in_progress", "closed"}, "closed": {"closed"}}
    if current not in transitions or target not in transitions[current]:
        raise InvalidTicket("Transition refusée : ouvrir → prendre en charge → clôturer.")
    return target
