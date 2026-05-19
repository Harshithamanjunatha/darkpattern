from flask import Flask, render_template
from flask_cors import CORS

from services.dataset_loader import load_dataset

from database.db import sessions_collection

from routes.stats_routes import stats_bp
from routes.alert_routes import alerts_bp
from routes.session_routes import sessions_bp
from routes.chart_routes import charts_bp
from services.ml_model import train_model
from routes.auth_routes import auth_bp
from routes.upload_routes import upload_bp
from routes.health_routes import health_bp
from routes.clickstream_routes import clickstream_bp
from routes.ingest_routes import ingest_bp
from routes.regenerate_routes import regenerate_bp

app = Flask(__name__)
app.secret_key = "darkpattern-secret-key-change-in-production"

CORS(app)

# Register Blueprints
app.register_blueprint(stats_bp)
app.register_blueprint(alerts_bp)
app.register_blueprint(sessions_bp)
app.register_blueprint(charts_bp)
app.register_blueprint(auth_bp)
app.register_blueprint(upload_bp)
app.register_blueprint(health_bp)
app.register_blueprint(clickstream_bp)
app.register_blueprint(ingest_bp)
app.register_blueprint(regenerate_bp)


@app.route("/")
def home():
    return render_template("home.html")


@app.route("/dashboard")
def dashboard():
    return render_template("index.html")

if __name__ == "__main__":

    train_model()

    if sessions_collection.count_documents({}) == 0:
        load_dataset()

    app.run(debug=True)