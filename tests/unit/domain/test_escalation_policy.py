import pytest
from pager.domain.models.escalation_policy import EscalationPolicy, EscalationLevel, NotificationTarget

def test_escalation_policy_creation():
    """
    Test case for creating an escalation policy.

    This test case verifies that an escalation policy can be created with the following properties:
    - A monitored service ID of 'service1'
    - One escalation level with a single notification target of type 'email' and address 'test@example.com'

    The test asserts the following:
    - The monitored service ID of the created policy is 'service1'
    - The policy has exactly one escalation level
    - The first escalation level has a single notification target of type 'email'
    """
    targets = [NotificationTarget(type='email', address='test@example.com')]
    level = EscalationLevel(targets=targets)
    policy = EscalationPolicy(monitored_service_id='service1', levels=[level])
    assert policy.monitored_service_id == 'service1'
    assert len(policy.levels) == 1
    assert policy.levels[0].targets[0].type == 'email'
