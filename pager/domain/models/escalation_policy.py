from dataclasses import dataclass, field
from typing import List

from pager.domain.models.notification_target import NotificationTarget
@dataclass
class EscalationLevel:
    targets: List[NotificationTarget]

@dataclass
class EscalationPolicy:
    monitored_service_id: str
    levels: List[EscalationLevel]
