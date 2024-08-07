from sentry.integrations.models.external_issue import ExternalIssue
from sentry.integrations.models.integration import Integration
from sentry.models.organization import Organization
from sentry.models.user import User
from sentry.silo.base import SiloMode
from sentry.tasks.base import instrumented_task, retry
from sentry.tasks.integrations.sync_assignee_outbound_impl import (
    sync_assignee_outbound as old_sync_assignee_outbound,
)


@instrumented_task(
    name="sentry.integrations.tasks.sync_assignee_outbound",
    queue="integrations",
    default_retry_delay=60 * 5,
    max_retries=5,
    silo_mode=SiloMode.REGION,
)
@retry(
    exclude=(
        ExternalIssue.DoesNotExist,
        Integration.DoesNotExist,
        User.DoesNotExist,
        Organization.DoesNotExist,
    )
)
def sync_assignee_outbound(external_issue_id: int, user_id: int | None, assign: bool) -> None:
    old_sync_assignee_outbound(external_issue_id=external_issue_id, user_id=user_id, assign=assign)
