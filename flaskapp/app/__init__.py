import os
from pathlib import Path

from flask import Flask

from app.config import Config

root_dir = None

def create_app(config_class=Config):
    global root_dir
    app = Flask(__name__, root_path=os.getcwd())
    app.config.from_object(config_class)

    app_dir = Path(app.root_path).parent.parent
    root_dir = os.path.join(app_dir, 'FlaskApp')

    # register blueprint here
    from app.rc_ocr.routes import rc_ocr
    app.register_blueprint(rc_ocr)

    return app
