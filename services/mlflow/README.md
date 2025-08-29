
# MLflow – Experiment Tracking & Leaderboard Logging

[MLflow](https://mlflow.org/) is used in this infrastructure as a centralized platform for **logging submission metrics**, **tracking experiments**, and optionally powering a **live leaderboard**.

Each submission, once evaluated, sends its results to MLflow as a tracked run. This enables easy comparison, visualization, and auditability of all challenge entries.

---

## Purpose

- Track evaluation metrics per submission (accuracy, F1, Dice, etc.)
- Visualize performance across tasks or participants
- Allow organizers to identify winners based on selected metrics
- Provide optional **real-time leaderboard** via UI or API


## Usage
Adjust the .env file to and configure the s3 storage backend [Garage}(../garage/) 
Start the MLflow tracking server:

```bash
docker compose -f docker-compose.mlflow.yml up -d
```

Use NGINX Proxy Manager to create a host like `mlflow.example.org` forwarding to `mlflow:5000`.
Web interface becomes available at:

```
https://mlflow.example.org
```

Seucre access via Authentik by setting up a Proxy Provider and Outpost as described in the [Authentik documentation](https://goauthentik.io/docs/providers/proxy/).


## Integration Flow (idea, not tested)

1. e.g. **Webhook in Gitea** triggers evaluation script
2. Evaluation script computes task-specific metrics
3. Metrics are sent to MLflow via Python API. See in [evaluation](/services/evaluation/inference/).
4. Organizers can view and compare submissions in the web UI


## Optional: Public Live Leaderboard via `/leaderboard.json`
> [!CAUTION] 
> Untested, idea only

Enable a transparent, real-time leaderboard by implementing a lightweight API endpoint (e.g., `/leaderboard.json`) that fetches top-performing submissions from MLflow and serves them in structured JSON format.

### How It Works

1. **Retrieve Top Runs Using MLflow's REST API**  
   Query MLflow's REST endpoint (`/api/2.0/mlflow/runs/search`) to fetch runs for a specific experiment, sorted by a performance metric like accuracy or Dice score.  
   This method leverages MLflow's native tracking capabilities for filtered and ordered run retrieval. 

2. **Build a Simple API Layer (e.g., Flask or FastAPI)**  
   Create an endpoint that:
   - Fetches runs via MLflow REST or Python API (`mlflow.search_runs()`)
   - Filters and sorts the top N runs
   - Outputs a JSON structure, for example:

   ```json
   {
     "leaderboard": [
       { "user": "teamA", "task": "phase1", "dice": 0.92 },
       { "user": "teamB", "task": "phase1", "dice": 0.89 }
     ]
   }
   ```

3. **Embed It Into Your Website**  
   Use JavaScript (or a React widget) to fetch and display the leaderboard in real-time:

   ```html
   <script>
     fetch('/leaderboard.json')
       .then((res) => res.json())
       .then((data) => renderLeaderboard(data.leaderboard));
   </script>
   ```

---

###  Advantages of This Approach

- Utilizes MLflow’s core tracking APIs — no additional infrastructure needed.
- Lightweight, flexible, and language/framework agnostic.
- Can anonymize or filter data per task to control visibility.
- Seamlessly integrates into existing web setups (WordPress, docs, etc.).


---

## Role in the Infrastructure

- Provides a reliable, extensible way to log and compare challenge results
- Serves as backend to final scoring and result tracking
- Promotes transparency and reproducibility for scientific challenges

---

## 📎 References

- [MLflow Docs](https://mlflow.org/docs/latest/index.html)
- [Tracking API](https://mlflow.org/docs/latest/tracking.html)
- [REST API Reference](https://mlflow.org/docs/latest/rest-api.html)

