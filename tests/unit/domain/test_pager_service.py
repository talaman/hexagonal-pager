import pytest
from unittest.mock import Mock
from pager.domain.models.escalation_policy import EscalationPolicy, EscalationLevel, NotificationTarget
from pager.domain.events import Alert
from pager.domain.services.pager_service import PagerService
from pager.ports.escalation_policy_repository import EscalationPolicyRepository
from pager.ports.email_sender import EmailSender
from pager.ports.sms_sender import SmsSender

@pytest.fixture
def policy_repo():
    return Mock(EscalationPolicyRepository)

@pytest.fixture
def email_sender():
    return Mock(EmailSender)

@pytest.fixture
def sms_sender():
    return Mock(SmsSender)

@pytest.fixture
def pager_service(policy_repo, email_sender, sms_sender):
    return PagerService(policy_repo, email_sender, sms_sender)

def test_handle_alert(pager_service, policy_repo, email_sender, sms_sender):
    """
    Test the handle_alert method of the PagerService class.
    Args:
        pager_service (PagerService): An instance of the PagerService class.
        policy_repo (PolicyRepository): An instance of the PolicyRepository class.
        email_sender (EmailSender): An instance of the EmailSender class.
        sms_sender (SmsSender): An instance of the SmsSender class.
    """
    targets = [NotificationTarget(type='email', address='test@example.com')]
    level = EscalationLevel(targets=targets)
    policy = EscalationPolicy(monitored_service_id='service1', levels=[level])
    
    policy_repo.get_policy.return_value = policy
    
    alert = Alert(service_id='service1', message='Test alert')
    pager_service.handle_alert(alert)
    
    email_sender.send.assert_called_once_with('test@example.com')
    sms_sender.send.assert_not_called()
