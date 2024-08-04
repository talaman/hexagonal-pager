# tests/unit/domain/test_monitored_service.py
import pytest
from pager.domain.models.monitored_service import MonitoredService

def test_monitored_service_creation():
    service = MonitoredService(id='service1', state='Healthy')
    assert service.id == 'service1'
    assert service.state == 'Healthy'
