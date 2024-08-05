import pytest
from unittest.mock import Mock
from pager.application.pager_application_service import PagerApplicationService
from pager.domain.events import Alert, Acknowledgement, HealthyEvent, Timeout
from pager.domain.services.pager_service import PagerService

@pytest.fixture
def pager_service():
    return Mock(PagerService)

@pytest.fixture
def pager_application_service(pager_service):
    return PagerApplicationService(pager_service)

def test_receive_alert(pager_application_service, pager_service):
    alert = Alert(service_id='service1', message='Test alert')
    pager_application_service.receive_alert(alert)
    pager_service.handle_alert.assert_called_once_with(alert)

def test_acknowledge_alert(pager_application_service, pager_service):
    ack = Acknowledgement(service_id='service1')
    pager_application_service.acknowledge_alert(ack)
    pager_service.handle_acknowledgement.assert_called_once_with(ack)

def test_healthy_event(pager_application_service, pager_service):
    event = HealthyEvent(service_id='service1')
    pager_application_service.healthy_event(event)
    pager_service.handle_healthy_event.assert_called_once_with(event)

def test_timeout(pager_application_service, pager_service):
    timeout = Timeout(service_id='service1')
    pager_application_service.timeout(timeout)
    pager_service.handle_timeout.assert_called_once_with(timeout.service_id)
