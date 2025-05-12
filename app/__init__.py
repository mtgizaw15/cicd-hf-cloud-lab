import os
from flask import Flask

def create_app():
    app = Flask(
        __name__,
        static_folder=os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
    )
    app.secret_key = 'titkos-kulcs'
    
    from .routes import main
    app.register_blueprint(main)

    return app