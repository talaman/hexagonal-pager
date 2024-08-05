import pytest
from pager.domain.models.escalation_policy import EscalationPolicy, EscalationLevel
from pager.domain.models.monitored_service import MonitoredService
from pager.domain.events import Alert, Acknowledgement, HealthyEvent
from pager.domain.models.notification_target import EmailTarget, SmsTarget
from pager.domain.services.pager_service import PagerService
from tests.mocks.mock_email_sender import MockEmailSender
from tests.mocks.mock_sms_sender import MockSmsSender
from tests.mocks.mock_escalation_policy_repository import MockEscalationPolicyRepository

@pytest.fixture
def setup_pager_service():
    email_sender = MockEmailSender()
    sms_sender = MockSmsSender()
    policy_repo = MockEscalationPolicyRepository({
        'service1': EscalationPolicy(
            monitored_service_id='service1',
            levels=[
                EscalationLevel(level_number=0, targets=[EmailTarget(email='test@example.com')]),
                EscalationLevel(level_number=1, targets=[SmsTarget(phone_number='1234567890')])
            ]
        )
    })
    pager_service = PagerService(policy_repo, email_sender, sms_sender)
    return pager_service, email_sender, sms_sender

def test_handle_alert(setup_pager_service):
    pager_service, email_sender, sms_sender = setup_pager_service
    alert = Alert(service_id='service1', message='Test Alert')
    
    pager_service.handle_alert(alert)
    
    assert len(email_sender.sent_emails) == 1
    assert email_sender.sent_emails[0] == 'test@example.com'

def test_handle_acknowledgement(setup_pager_service):
    pager_service, email_sender, sms_sender = setup_pager_service
    alert = Alert(service_id='service1', message='Test Alert')
    pager_service.handle_alert(alert)

    ack = Acknowledgement(service_id='service1')
    pager_service.handle_acknowledgement(ack)

    service = pager_service.monitored_services['service1']
    assert service.acknowledged

def test_handle_healthy_event(setup_pager_service):
    pager_service, email_sender, sms_sender = setup_pager_service
    alert = Alert(service_id='service1', message='Test Alert')
    pager_service.handle_alert(alert)

    healthy_event = HealthyEvent(service_id='service1')
    pager_service.handle_healthy_event(healthy_event)

    service = pager_service.monitored_services['service1']
    assert service.state == 'Healthy'

def test_handle_timeout(setup_pager_service):
    pager_service, email_sender, sms_sender = setup_pager_service
    alert = Alert(service_id='service1', message='Test Alert')
    pager_service.handle_alert(alert)

    pager_service.handle_timeout('service1')

    assert len(sms_sender.sent_sms) == 1
    assert sms_sender.sent_sms[0] == '1234567890'
