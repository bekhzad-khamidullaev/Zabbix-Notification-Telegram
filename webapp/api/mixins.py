from ..utils.models import AuditLog


class AuditLogMixin:
    def log_action(self, instance, action):
        AuditLog.objects.create(
            user=self.request.user,
            action=f"{instance._meta.model_name}.{action}",
            details={"id": instance.pk},
        )
