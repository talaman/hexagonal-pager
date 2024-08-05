from dataclasses import dataclass

@dataclass
class Alert:
    service_id: str
    message: str

@dataclass
class Acknowledgement:
    service_id: str

@dataclass
class HealthyEvent:
    service_id: str

@dataclass
class Timeout:
    service_id: str
