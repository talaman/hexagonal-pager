import pytest
from pager.domain.models.monitored_service import MonitoredService

def test_mark_unhealthy():
    service = MonitoredService(id='service1')
    service.mark_unhealthy()
    assert service.state == 'Unhealthy'
    assert not service.acknowledged
    assert service.current_level == 0

def test_mark_healthy():
    service = MonitoredService(id='service1', state='Unhealthy', acknowledged=False)
    service.mark_healthy()
    assert service.state == 'Healthy'
    assert not service.acknowledged

def test_acknowledge_alert():
    service = MonitoredService(id='service1', state='Unhealthy', acknowledged=False)
    service.acknowledge_alert()
    assert service.acknowledged
