from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from pager.domain.models.escalation_policy import EscalationLevel, EscalationPolicy
from pager.domain.models.notification_target import EmailTarget, SmsTarget
from pager.domain.services.pager_service import PagerService
from pager.domain.events import Alert, Acknowledgement, HealthyEvent
from pager.ports.email_sender import EmailSender
from pager.ports.sms_sender import SmsSender
from pager.ports.escalation_policy_repository import EscalationPolicyRepository
from tests.mocks.mock_escalation_policy_repository import MockEscalationPolicyRepository

app = FastAPI()

# Initialize the PagerService
policy_repo = MockEscalationPolicyRepository({
        'service1': EscalationPolicy(
            monitored_service_id='service1',
            levels=[
                EscalationLevel(level_number=0, targets=[EmailTarget(email='test@example.com')]),
                EscalationLevel(level_number=1, targets=[SmsTarget(phone_number='1234567890')])
            ]
        )
    })
email_sender = EmailSender()
sms_sender = SmsSender()

pager_service = PagerService(policy_repo, email_sender, sms_sender)

class AlertRequest(BaseModel):
    service_id: str
    message: str

class AcknowledgementRequest(BaseModel):
    service_id: str

class HealthyEventRequest(BaseModel):
    service_id: str

@app.post("/alert")
def receive_alert(request: AlertRequest):
    alert = Alert(service_id=request.service_id, message=request.message)
    pager_service.handle_alert(alert)
    return {"status": "Alert received"}

@app.post("/acknowledge")
def acknowledge_alert(request: AcknowledgementRequest):
    acknowledgement = Acknowledgement(service_id=request.service_id)
    pager_service.handle_acknowledgement(acknowledgement)
    return {"status": "Acknowledgement received"}

@app.post("/healthy")
def healthy_event(request: HealthyEventRequest):
    healthy_event = HealthyEvent(service_id=request.service_id)
    pager_service.handle_healthy_event(healthy_event)
    return {"status": "Healthy event received"}

