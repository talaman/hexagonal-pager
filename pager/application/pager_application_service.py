from pager.domain.services.pager_service import PagerService
from pager.domain.events import Alert, Acknowledgement, HealthyEvent, Timeout

class PagerApplicationService:
    def __init__(self, pager_service: PagerService):
        self.pager_service = pager_service

    def receive_alert(self, alert: Alert):
        self.pager_service.handle_alert(alert)

    def acknowledge_alert(self, ack: Acknowledgement):
        # Handle acknowledgement logic
        pass

    def healthy_event(self, event: HealthyEvent):
        # Handle healthy event logic
        pass

    def timeout(self, timeout: Timeout):
        # Handle timeout logic
        pass
