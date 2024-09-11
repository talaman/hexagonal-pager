from dataclasses import dataclass
from abc import ABC, abstractmethod

class NotificationTarget(ABC):
    @abstractmethod
    def get_contact_info(self) -> str:
        pass

@dataclass
class EmailTarget(NotificationTarget):
    email: str

    def get_contact_info(self) -> str:
        return self.email

@dataclass
class SmsTarget(NotificationTarget):
    phone_number: str

    def get_contact_info(self) -> str:
        return self.phone_number
    
@dataclass
class SlackTarget(NotificationTarget):
    channel: str

    def get_contact_info(self) -> str:
        return self.channel