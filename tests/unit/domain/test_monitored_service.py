import pytest
from pager.domain.models.monitored_service import MonitoredService

def test_monitored_service_creation():
    """
    Test case for creating a MonitoredService object.

    This test verifies that a MonitoredService object can be created with the specified id and state.
    It checks that the id and state attributes of the created object match the provided values.

    """
    service = MonitoredService(id='service1', state='Healthy')
    assert service.id == 'service1'
    assert service.state == 'Healthy'
