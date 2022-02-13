from flask import Flask


def init_app():
    """Construct core Flask application."""
    app = Flask(__name__, instance_relative_config=False)

    with app.app_context():
        # Import Dash application
        from dash_app import init_dashboard
        app = init_dashboard(app)

        return app