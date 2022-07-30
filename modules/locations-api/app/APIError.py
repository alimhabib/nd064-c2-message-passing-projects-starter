import traceback
import app
from jsonify import jsonify 

class APIError(Exception):
    """All custom API Exceptions"""
    pass


class APIAuthError(APIError):
    """Custom Authentication Error Class."""
    code = 403
    description = "Authentication Error"


@app.errorhandler(APIError)
def handle_exception(err):
    """Return custom JSON when APIError or its children are raised"""
    response = {"error": err.description, "message": ""}
    if len(err.args) > 0:
        response["message"] = err.args[0]
    # Add some logging so that we can monitor different types of errors 
    app.logger.error(f"{err.description}: {response['message']}" )
    return jsonify(response), err.code

@app.errorhandler(500)
def handle_exception(err):
    """Return JSON instead of HTML for any other server error"""
    app.logger.error(f"Unknown Exception: {str(err)}")
    app.logger.debug(''.join(traceback.format_exception(etype=type(err), value=err, tb=err.__traceback__)))
    response = {"error": "Unexpected error"}
    return jsonify(response), 500