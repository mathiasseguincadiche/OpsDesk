import pytest

from app.workflow import TransitionError, allowed_transitions, check_transition


def test_staff_full_lifecycle():
    for current, target in [("open", "in_progress"), ("in_progress", "resolved"), ("resolved", "closed"), ("closed", "open")]:
        check_transition(current, target, is_staff=True)


@pytest.mark.parametrize("current,target", [("open", "resolved"), ("closed", "in_progress"), ("open", "open")])
def test_invalid_transitions(current, target):
    with pytest.raises(TransitionError):
        check_transition(current, target, is_staff=True)


def test_requester_limited():
    with pytest.raises(PermissionError):
        check_transition("open", "in_progress", is_staff=False)
    check_transition("resolved", "closed", is_staff=False)
    check_transition("resolved", "in_progress", is_staff=False)
    assert allowed_transitions("resolved", is_staff=False) == ["in_progress", "closed"]
    assert allowed_transitions("closed", is_staff=False) == []
