from typing import List, Dict
from pager.domain.models.escalation_policy import EscalationPolicy
from pager.domain.models.monitored_service import MonitoredService
from pager.domain.events import Alert, Acknowledgement, HealthyEvent, Timeout
from pager.domain.models.notification_target import NotificationTarget, EmailTarget, SmsTarget
from pager.ports.email_sender import EmailSender
from pager.ports.sms_sender import SmsSender
from pager.ports.escalation_policy_repository import EscalationPolicyRepository

class PagerService:
    def __init__(self, policy_repo: EscalationPolicyRepository, email_sender: EmailSender, sms_sender: SmsSender):
        """
        Initializes a PagerService object.

        Args:
            policy_repo (EscalationPolicyRepository): The repository for escalation policies.
            email_sender (EmailSender): The email sender object.
            sms_sender (SmsSender): The SMS sender object.
        """
        self.policy_repo = policy_repo
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.monitored_services: Dict[str, MonitoredService] = {}

    def handle_alert(self, alert: Alert):
        """
        Handles an alert by marking the corresponding service as unhealthy, notifying the targets, and starting an acknowledgment timer.

        Parameters:
        - alert (Alert): The alert to handle.

        Returns:
        - None
        """
        service = self.get_or_create_monitored_service(alert.service_id)
        if service.state == "Healthy":
            service.mark_unhealthy()
            policy = self.policy_repo.get_policy(alert.service_id)
            self.notify_targets(policy.get_first_level().targets)
            service.start_acknowledgment_timer(15 * 60, lambda: self.handle_timeout(alert.service_id))

    def handle_acknowledgement(self, ack: Acknowledgement):
        """
        Handles the acknowledgement of an alert.

        Parameters:
            ack (Acknowledgement): The acknowledgement object containing the service ID.

        Returns:
            None
        """
        service = self.get_or_create_monitored_service(ack.service_id)
        if service.state == "Unhealthy":
            service.acknowledge_alert()

    def handle_healthy_event(self, event: HealthyEvent):
        """
        Handles a healthy event by marking the corresponding service as healthy.

        Parameters:
            event (HealthyEvent): The healthy event to handle.

        Returns:
            None
        """
        service = self.get_or_create_monitored_service(event.service_id)
        service.mark_healthy()

    def handle_timeout(self, service_id: str):
        """
        Handles the timeout event for a specific service.

        Args:
            service_id (str): The ID of the service.

        Raises:
            ValueError: If there are no more levels to escalate to.

        """
        service = self.monitored_services[service_id]
        if service.state == "Unhealthy" and not service.acknowledged:
            policy = self.policy_repo.get_policy(service_id)
            try:
                next_level = policy.get_next_level(service.current_level)
                self.notify_targets(next_level.targets)
                service.current_level += 1
                service.start_acknowledgment_timer(15 * 60, lambda: self.handle_timeout(service_id))
            except ValueError:
                # No more levels to escalate to
                pass

    def notify_targets(self, targets: List[NotificationTarget]):
        """
        Notifies the given list of targets.

        Args:
            targets (List[NotificationTarget]): A list of NotificationTarget objects.

        Returns:
            None
        """
        for target in targets:
            if isinstance(target, EmailTarget):
                self.email_sender.send(target.get_contact_info())
            elif isinstance(target, SmsTarget):
                self.sms_sender.send(target.get_contact_info())

    def get_or_create_monitored_service(self, service_id: str) -> MonitoredService:
        """
        Retrieves or creates a monitored service based on the given service ID.

        Parameters:
            service_id (str): The ID of the service.

        Returns:
            MonitoredService: The retrieved or created monitored service.
        """
        if service_id not in self.monitored_services:
            self.monitored_services[service_id] = MonitoredService(id=service_id)
        return self.monitored_services[service_id]
