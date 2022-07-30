import os
from flask_sqlalchemy import SQLAlchemy

from app import create_app

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    ## stream logs to a file
    logging.basicConfig(
    format='%(levelname)-8s : %(asctime)s  %(message)s',
    level=logging.DEBUG,
    datefmt='%Y-%m-%d %H:%M:%S', handlers=[ 
        logging.StreamHandler(sys.stdout),
        logging.StreamHandler(sys.stderr)
    ]) 
    @app.errorhandler(SQLAlchemyError)
    def handle_exception(err):
        """Handle DB connection errors """
        if isinstance(err, sqlalchemy.exc.InternalError):
            response["message"] = "Unable to connect to DB"
        return jsonify(response), 555
    app.run(debug=True)
