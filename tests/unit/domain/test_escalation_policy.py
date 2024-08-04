# tests/unit/domain/test_escalation_policy.py
import pytest
from pager.domain.models.escalation_policy import EscalationPolicy, EscalationLevel, NotificationTarget

def test_escalation_policy_creation():
    targets = [NotificationTarget(type='email', address='test@example.com')]
    level = EscalationLevel(targets=targets)
    policy = EscalationPolicy(monitored_service_id='service1', levels=[level])
    assert policy.monitored_service_id == 'service1'
    assert len(policy.levels) == 1
    assert policy.levels[0].targets[0].type == 'email'
