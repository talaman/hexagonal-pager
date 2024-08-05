import pytest
from tests.unit.application.use_case_scenarios import MonitoredService, Pager

def test_alert_healthy_to_unhealthy():
    # Given a Monitored Service in a Healthy State,
    # when the Pager receives an Alert related to this Monitored Service,
    # then the Monitored Service becomes Unhealthy,
    # the Pager notifies all targets of the first level of the escalation policy,
    # and sets a 15-minutes acknowledgement delay
    service = MonitoredService()
    pager = Pager()
    
    pager.receive_alert(service)
    
    assert service.state == 'Unhealthy'
    assert pager.targets_notified == [1]
    assert pager.acknowledgement_delay == 15

def test_acknowledgement_timeout_unhealthy():
    # Given a Monitored Service in an Unhealthy State,
    # the corresponding Alert is not Acknowledged
    # and the last level has not been notified,
    # when the Pager receives the Acknowledgement Timeout,
    # then the Pager notifies all targets of the next level of the escalation policy
    # and sets a 15-minutes acknowledgement delay.
    service = MonitoredService()
    service.set_state('Unhealthy')
    pager = Pager()
    
    pager.receive_acknowledgement_timeout(service, last_level_notified=False)
    
    assert pager.targets_notified == [2]
    assert pager.acknowledgement_delay == 15

def test_acknowledgement_timeout_after_acknowledgement():
    # Given a Monitored Service in an Unhealthy State
    # when the Pager receives the Acknowledgement
    # and later receives the Acknowledgement Timeout,
    # then the Pager doesn't notify any Target
    # and doesn't set an acknowledgement delay.
    service = MonitoredService()
    service.set_state('Unhealthy')
    pager = Pager()
    
    pager.receive_acknowledgement(service)
    pager.receive_acknowledgement_timeout(service, last_level_notified=True)
    
    assert pager.targets_notified == []
    assert pager.acknowledgement_delay == 0

def test_alert_unhealthy_state():
    # Given a Monitored Service in an Unhealthy State,
    # when the Pager receives an Alert related to this Monitored Service,
    # then the Pager doesn’t notify any Target
    # and doesn’t set an acknowledgement delay
    service = MonitoredService()
    service.set_state('Unhealthy')
    pager = Pager()
    
    pager.receive_alert(service)
    
    assert pager.targets_notified == []
    assert pager.acknowledgement_delay == 0

def test_healthy_event_unhealthy_state():
    # Given a Monitored Service in an Unhealthy State,
    # when the Pager receives a Healthy event related to this Monitored Service
    # and later receives the Acknowledgement Timeout,
    # then the Monitored Service becomes Healthy,
    # the Pager doesn’t notify any Target
    # and doesn’t set an acknowledgement delay
    service = MonitoredService()
    service.set_state('Unhealthy')
    pager = Pager()
    
    pager.receive_healthy_event(service)
    pager.receive_acknowledgement_timeout(service, last_level_notified=True)
    
    assert service.state == 'Healthy'
    assert pager.targets_notified == []
    assert pager.acknowledgement_delay == 0