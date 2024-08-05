from dataclasses import dataclass

@dataclass
class NotificationTarget:
    type: str  # 'email' or 'sms'
    address: str  # email address or phone number