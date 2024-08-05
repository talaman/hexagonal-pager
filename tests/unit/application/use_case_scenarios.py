class MonitoredService:
    def __init__(self):
        self.state = 'Healthy'

    def set_state(self, state):
        self.state = state

class Pager:
    def __init__(self):
        self.acknowledgement_delay = 0
        self.targets_notified = []

    def receive_alert(self, service):
        if service.state == 'Healthy':
            service.set_state('Unhealthy')
            self.notify_targets(level=1)
            self.acknowledgement_delay = 15
        elif service.state == 'Unhealthy':
            pass

    def receive_acknowledgement_timeout(self, service, last_level_notified):
        if service.state == 'Unhealthy' and not last_level_notified:
            self.notify_targets(level=2)
            self.acknowledgement_delay = 15

    def receive_acknowledgement(self, service):
        pass

    def receive_healthy_event(self, service):
        if service.state == 'Unhealthy':
            service.set_state('Healthy')

    def notify_targets(self, level):
        self.targets_notified.append(level)