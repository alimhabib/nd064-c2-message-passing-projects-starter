import os 
import logging 
import sys 
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
    app.run(debug=True)