from flask import Flask
from marketdata_api.config import FLASK_ENV
from marketdata_api.database.base import init_db, DB_PATH

def create_app():
    app = Flask(__name__,
                template_folder="../frontend/templates",
                static_folder="../frontend/static")
    app.config["ENV"] = FLASK_ENV

    # Initialize database and create tables
    print("Initializing database...")
    init_db()
    print("Database initialization complete")

    from marketdata_api.routes.market import market_bp
    from marketdata_api.routes.schema import schema_bp
    app.register_blueprint(market_bp)
    app.register_blueprint(schema_bp)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=(FLASK_ENV == "development"))