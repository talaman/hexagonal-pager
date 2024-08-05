from typing import List
from pager.domain.models.escalation_policy import EscalationPolicy
from pager.domain.models.monitored_service import MonitoredService
from pager.domain.events import Alert, Acknowledgement, HealthyEvent, Timeout
from pager.domain.models.notification_target import NotificationTarget
from pager.ports.email_sender import EmailSender
from pager.ports.sms_sender import SmsSender
from pager.ports.escalation_policy_repository import EscalationPolicyRepository

class PagerService:
    def __init__(self, policy_repo: EscalationPolicyRepository, email_sender: EmailSender, sms_sender: SmsSender):
        self.policy_repo = policy_repo
        self.email_sender = email_sender
        self.sms_sender = sms_sender

    def handle_alert(self, alert: Alert):
        policy = self.policy_repo.get_policy(alert.service_id)
        if policy:
            self.notify_targets(policy.levels[0].targets)

    def notify_targets(self, targets: List[NotificationTarget]):
        for target in targets:
            if target.type == 'email':
                self.email_sender.send(target.address)
            elif target.type == 'sms':
                self.sms_sender.send(target.address)
