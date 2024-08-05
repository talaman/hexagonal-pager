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
        self.policy_repo = policy_repo
        self.email_sender = email_sender
        self.sms_sender = sms_sender
        self.monitored_services: Dict[str, MonitoredService] = {}

    def handle_alert(self, alert: Alert):
        service = self.get_or_create_monitored_service(alert.service_id)
        if service.state == "Healthy":
            service.mark_unhealthy()
            policy = self.policy_repo.get_policy(alert.service_id)
            self.notify_targets(policy.get_first_level().targets)
            service.start_acknowledgment_timer(15 * 60, lambda: self.handle_timeout(alert.service_id))

    def handle_acknowledgement(self, ack: Acknowledgement):
        service = self.get_or_create_monitored_service(ack.service_id)
        if service.state == "Unhealthy":
            service.acknowledge_alert()

    def handle_healthy_event(self, event: HealthyEvent):
        service = self.get_or_create_monitored_service(event.service_id)
        service.mark_healthy()

    def handle_timeout(self, service_id: str):
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
        for target in targets:
            if isinstance(target, EmailTarget):
                self.email_sender.send(target.get_contact_info())
            elif isinstance(target, SmsTarget):
                self.sms_sender.send(target.get_contact_info())

    def get_or_create_monitored_service(self, service_id: str) -> MonitoredService:
        if service_id not in self.monitored_services:
            self.monitored_services[service_id] = MonitoredService(id=service_id)
        return self.monitored_services[service_id]
