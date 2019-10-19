from flask import Blueprint
from flask import render_template
from flask import session


errors = Blueprint('errors', __name__)


@errors.app_errorhandler(401)
@errors.app_errorhandler(403)
@errors.app_errorhandler(404)
def default_error_handler(e):
    return render_template("error.html",
                           title="Error "+str(e.code),
                           error_code=str(e.code),
                           error_name=str(e.name),
                           error_description=str(e.description))
