# Automated Evaluation Pipeline

This section describes a high-level workflow to automatically run each participant's containerized submission, compare its outputs to the ground truth, calculate performance metrics, and track the results. By organizing the [evaluation in a script](./evaluate.py), you can ensure all submissions are evaluated consistently while managing computational resources.

## Running Submissions Sequentially
Manage your ressources!
To avoid exhausting your GPU or CPU resources, run the submissions one by one (consecutively) instead of all at once. You can either use your existing GPU job scheduling system or write a script to iterate through each submission directory. Assuming each submission resides in its own folder under a common submissions/ directory, the script can perform the following steps for each submission.
> [!NOTE]
> Wait for Completion: Ensure the container finishes before moving to the next submission. This can be done by running Docker in attached mode (so the docker-compose up command blocks until completion) or by running in detached mode and then polling for container status. For example, after docker-compose up -d, the script might use docker-compose ps -q to get the container ID and then call docker wait <container_id> to pause the script until that container exits. This guarantees each submission is processed one at a time, preventing resource conflicts.

### Output Comparison and Metrics Calculation

After a submission's container has run, it will produce an output folder (e.g., containing prediction files such as images or results for that task).
> [!CAUTION]
>Dealing with Errors:
> Currently there is no feedback to the participant during this process. They will not get informed if an error occurs. If the output directory stays empty, you should forward the dc.log file (e.g., email or Gitea issue) to the participant so they have to debug their submission.
The next step is to compare these outputs against the ground truth data to evaluate the submission's performance. 

For each pair of output vs ground truth, compute relevant evaluation metrics. The choice of metrics will depend on the task (classification, segmentation, etc.).
> [!TIP]
>We recommend referring to literature on evaluation metrics for your specific domain to choose the right ones.
>For Image Analysis we recommend [Metrics Reloaded](https://pmc.ncbi.nlm.nih.gov/articles/PMC11182665/pdf/nihms-1998267.pdf).

Summarize the metrics for the submission. This could mean averaging per-image metrics into an overall score or computing separate metrics for different categories. You may also want to output a score or a set of scores that will form the basis of your leaderboard.

## Logging Results with MLflow

Instead of manually keeping track of scores, we recommend using a state-of-the-art experiment tracking tool like MLflow to log your metrics and results. MLflow allows you to record the metrics for each submission (each container run) in a structured way. See the [MLflow Server Setup](/services/mlflow/) for instructions on deploying an MLflow server in your infrastructure.
> See [MLflow Tracking API](https://www.mlflow.org/docs/latest/tracking.html) for details.

- **Organized Experiment Tracking** You can create an MLflow experiment (e.g., named "Submission Evaluation") and log each submission's results as an individual run. For each run, log parameters such as the submission identifier or any configuration info, and log the performance metrics computed in the previous step.

- **Sharing the Leaderboard** Once the metrics are logged in MLflow, you have several options to share the results. You could host the MLflow tracking server and share its interface with participants or stakeholders. Alternatively, you can export the metrics and create a static leaderboard on your website. For instance, you might use MLflow's API to retrieve the latest scores and then embed them on your WordPress site. This way, the leaderboard on your site can be kept up-to-date with the evaluation results.