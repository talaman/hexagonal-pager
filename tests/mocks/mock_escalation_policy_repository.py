from pager.ports.escalation_policy_repository import EscalationPolicyRepository
from pager.domain.models.escalation_policy import EscalationPolicy

class MockEscalationPolicyRepository(EscalationPolicyRepository):
    def __init__(self, policies):
        self.policies = policies

    def get_policy(self, service_id: str) -> EscalationPolicy:
        return self.policies.get(service_id)
