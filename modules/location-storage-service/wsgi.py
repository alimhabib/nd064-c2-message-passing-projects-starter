import os

import werkzeug
werkzeug.cached_property = werkzeug.utils.cached_property
from app import create_app

app = create_app(os.getenv("FLASK_ENV") or "test")
if __name__ == "__main__":
    app.run(debug=True)
