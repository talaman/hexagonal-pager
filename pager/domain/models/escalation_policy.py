from dataclasses import dataclass, field
from typing import List
from pager.domain.models.notification_target import NotificationTarget

@dataclass
class EscalationLevel:
    level_number: int
    targets: List[NotificationTarget]

@dataclass
class EscalationPolicy:
    monitored_service_id: str
    levels: List[EscalationLevel]

    def get_first_level(self) -> EscalationLevel:
        if self.levels:
            return self.levels[0]
        raise ValueError("No levels defined in the escalation policy")

    def get_next_level(self, current_level: int) -> EscalationLevel:
        if current_level < len(self.levels) - 1:
            return self.levels[current_level + 1]
        raise ValueError("No more levels in the escalation policy")
