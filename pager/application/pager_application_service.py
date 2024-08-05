from pager.domain.services.pager_service import PagerService
from pager.domain.events import Alert, Acknowledgement, HealthyEvent, Timeout

class PagerApplicationService:
    def __init__(self, pager_service: PagerService):
        self.pager_service = pager_service

    def receive_alert(self, alert: Alert):
        """
        Process an incoming alert.
        
        This method delegates the handling of the alert to the PagerService, which will:
        - Update the monitored service state
        - Notify the targets according to the escalation policy
        - Start the acknowledgment timer
        """
        self.pager_service.handle_alert(alert)

    def acknowledge_alert(self, ack: Acknowledgement):
        """
        Process an acknowledgment of an alert.
        
        This method delegates the acknowledgment handling to the PagerService, which will:
        - Update the monitored service state
        - Ensure no further notifications are sent for this alert
        """
        self.pager_service.handle_acknowledgement(ack)

    def healthy_event(self, event: HealthyEvent):
        """
        Process a healthy event.
        
        This method delegates the handling of the healthy event to the PagerService, which will:
        - Update the monitored service state to Healthy
        - Stop any ongoing acknowledgment timers
        """
        self.pager_service.handle_healthy_event(event)

    def timeout(self, timeout: Timeout):
        """
        Process an acknowledgment timeout.
        
        This method delegates the timeout handling to the PagerService, which will:
        - Escalate to the next level in the escalation policy
        - Notify the targets at the new level
        """
        self.pager_service.handle_timeout(timeout.service_id)
