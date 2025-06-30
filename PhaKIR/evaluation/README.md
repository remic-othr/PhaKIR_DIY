Herunterladen und Sortieren von Modellen aus docker-registry
siehe prepare.py


Typisches Vorgehen (am Beispiel MLflow):
Ausführen deines Modells (z.B. in Docker):

Ergebnisse werden in CSV oder JSON geschrieben.

Metriken berechnen (auch via Bootstrapping):

Python-Skript berechnet statistische Auswertungen.

Ergebnisse in MLflow loggen:

python
Kopieren
Bearbeiten
import mlflow

mlflow.set_experiment("Project Metrics")

with mlflow.start_run(run_name="model_v1"):
    mlflow.log_param("model_name", "model_v1")
    mlflow.log_metric("accuracy", 0.85)
    mlflow.log_metric("precision_mean", 0.83)
    mlflow.log_metric("precision_std", 0.02)
Leaderboard/Web-Integration:

MLflow hat eine REST-API zur Integration mit Web-Frontends.

Ergebnisse als Web-Frontend darstellen (z.B. via Streamlit oder FastAPI).