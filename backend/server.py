from flask import Flask
from backend.api import archives_api

def create_app():
    app = Flask(__name__)

    # Register all blueprints
    app.register_blueprint(archives_api.bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)
