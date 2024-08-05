from dataclasses import dataclass

@dataclass
class MonitoredService:
    id: str
    state: str  # 'Healthy' or 'Unhealthy'
