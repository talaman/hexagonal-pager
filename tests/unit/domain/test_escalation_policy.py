import pytest
from pager.domain.models.escalation_policy import EscalationPolicy, EscalationLevel
from pager.domain.models.notification_target import EmailTarget, SmsTarget

def test_escalation_policy_creation():
    """
    Test case for creating an escalation policy with email and SMS targets.
    """
    email_target = EmailTarget(email='test@example.com')
    sms_target = SmsTarget(phone_number='1234567890')
    level1 = EscalationLevel(level_number=0, targets=[email_target])
    level2 = EscalationLevel(level_number=1, targets=[sms_target])
    policy = EscalationPolicy(monitored_service_id='service1', levels=[level1, level2])
    
    assert policy.monitored_service_id == 'service1'
    assert len(policy.levels) == 2
    assert isinstance(policy.levels[0].targets[0], EmailTarget)
    assert isinstance(policy.levels[1].targets[0], SmsTarget)

def test_get_first_level():
    email_target = EmailTarget(email='test@example.com')
    level = EscalationLevel(level_number=0, targets=[email_target])
    policy = EscalationPolicy(monitored_service_id='service1', levels=[level])
    
    first_level = policy.get_first_level()
    assert first_level == level

def test_get_next_level():
    email_target = EmailTarget(email='test@example.com')
    sms_target = SmsTarget(phone_number='1234567890')
    level1 = EscalationLevel(level_number=0, targets=[email_target])
    level2 = EscalationLevel(level_number=1, targets=[sms_target])
    policy = EscalationPolicy(monitored_service_id='service1', levels=[level1, level2])
    
    next_level = policy.get_next_level(0)
    assert next_level == level2

def test_get_next_level_no_more_levels():
    email_target = EmailTarget(email='test@example.com')
    level = EscalationLevel(level_number=0, targets=[email_target])
    policy = EscalationPolicy(monitored_service_id='service1', levels=[level])
    
    with pytest.raises(ValueError):
        policy.get_next_level(0)
