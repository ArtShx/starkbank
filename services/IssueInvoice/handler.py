"""
Serverless function to issue invoices for random users.
"""

import functions_framework

from datetime import datetime
import os
from random import randint

from google.cloud import scheduler_v1
from google.cloud.scheduler_v1.types import Job

from starkbank_integration.auth import Authentication
from starkbank_integration.environment import Environment
from starkbank_integration.exceptions import ErrorCreatingInvoice
from starkbank_integration.invoice import Invoice, InvoiceCreateRequest
from starkbank_integration.db.base import BaseDB


@functions_framework.http
def entrypoint(request):
    """HTTP Cloud Function.
    Args:
        request (flask.Request): The request object.
        <https://flask.palletsprojects.com/en/1.1.x/api/#incoming-request-data>
    Returns:
        The response text, or any set of values that can be turned into a
        Response object using `make_response`
        <https://flask.palletsprojects.com/en/1.1.x/api/#flask.make_response>.
    """
    payload = request.get_json()
    forced_execution = payload.get("force", False)
    if not should_run() and not forced_execution:
        disable_scheduler()
        return {"msg": "Service are configured to not run now, leaving."}
    success = handler()
    return {"success": success}


def should_run() -> bool:
    """
    Checks if this job should be running now by looking at the Datastore configuration.
    Maybe we should use something stored in Redis for efficience and more appropriate for this task.
    """
    db = BaseDB("IssueInvoiceConfig")
    config = db.get_all(limit=1)[0]

    end_time = config["end_time"]
    # Converting DatetimeWithNanoSeconds to datetime
    end_time = datetime.fromtimestamp(end_time.timestamp())
    now = datetime.utcnow()
    return now < end_time


def disable_scheduler() -> bool:
    """Pauses a scheduled job from GCP Cloud Scheduler."""
    env_file = os.environ["env_file"]
    env = Environment.from_file(env_file)
    job_name = f"projects/{env['gcp_project']}/locations/{env['gcp_location']}/jobs/IssueInvoice"
    client = scheduler_v1.CloudSchedulerClient()
    request = scheduler_v1.PauseJobRequest(name=job_name)
    response = client.pause_job(request=request)

    return response.state == Job.State.PAUSED


def handler():
    """Creates 8-12 invoices to random peoples."""
    Authentication.init()
    nb_users_to_send = randint(8, 12)

    db = BaseDB("User")
    user_data = db.get_all(limit=nb_users_to_send)

    inv_req = [
        InvoiceCreateRequest(
            user["name"], user["user_type"], user["tax_id"], amount=randint(1, 1000)
        )
        for user in user_data
    ]
    try:
        Invoice.create(inv_req)
        return True
    except ErrorCreatingInvoice:
        return False


if __name__ == "__main__":
    entrypoint(None)
