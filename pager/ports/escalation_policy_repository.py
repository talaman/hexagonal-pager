from pager.domain.models.escalation_policy import EscalationPolicy

class EscalationPolicyRepository:
    def get_policy(self, service_id: str) -> EscalationPolicy:
        pass
