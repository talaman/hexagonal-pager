from dataclasses import dataclass, field
from typing import Optional
from threading import Timer

@dataclass
class MonitoredService:
    id: str
    state: str = "Healthy"  # 'Healthy' or 'Unhealthy'
    acknowledged: bool = False
    current_level: int = 0
    timer: Optional[Timer] = field(default=None, init=False, repr=False)

    def mark_unhealthy(self):
        self.state = "Unhealthy"
        self.acknowledged = False
        self.current_level = 0

    def mark_healthy(self):
        self.state = "Healthy"
        self.acknowledged = False
        self.cancel_timer()

    def acknowledge_alert(self):
        self.acknowledged = True
        self.cancel_timer()

    def start_acknowledgment_timer(self, timeout: int, timeout_callback):
        self.cancel_timer()
        self.timer = Timer(timeout, timeout_callback)
        self.timer.start()

    def cancel_timer(self):
        if self.timer:
            self.timer.cancel()
            self.timer = None
