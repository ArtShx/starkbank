"""
Hello World service to test if everything is working as expected.
"""

import functions_framework

from starkbank_integration.auth import Authentication
from starkbank_integration import __version__ as version


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
    success, err = Authentication.test()
    return {
        "auth_success": success,
        "auth_message": err,
        "starkbank_integration_version": version,
    }
