# tests/unit/application/test_pager_application_service.py
import pytest
from unittest.mock import Mock
from pager.application.pager_application_service import PagerApplicationService
from pager.domain.events import Alert
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
