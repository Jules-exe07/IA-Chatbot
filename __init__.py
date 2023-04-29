from flask import Flask

# Create Flask app instance
def create_app():
    app = Flask(__name__)

    # Set a secret key to enable session management
    app.config['SECRET_KEY'] = 'Here we go again boi'

    # Import and register blueprints for different views and functionalities
    from .views import views
    from .auth import auth

    app.register_blueprint(views, url_prefix='/')
    app.register_blueprint(auth, url_prefix='/')

    # Return the created app instance
    return app
