import os
import subprocess
import time
from pathlib import Path
import mlflow

# Configure MLFlow experiment
mlflow.set_experiment("Submission_Evaluation")  # creates or uses an experiment

# Paths configuration
SUBMISSIONS_DIR = Path("submissions")
GROUND_TRUTH_DIR = Path("ground_truth")  # path to ground truth data

# Placeholder for metric calculation function
def calculate_metrics(output_dir: Path, gt_dir: Path):
    """
    Compare the outputs in output_dir with the ground truth in gt_dir and 
    return a dictionary of metric scores. This function should be implemented 
    according to the specific evaluation metrics of the task.
    """
    # TODO: Implement the actual metric computations (e.g., IoU, Dice, accuracy, etc.)
    # For now, we return a dummy result for illustration.
    dummy_metrics = {
        "score": 0.0  # replace with actual metrics like "mean_iou" or "accuracy"
    }
    return dummy_metrics

# Iterate over each submission folder
for submission_path in SUBMISSIONS_DIR.iterdir():
    if not submission_path.is_dir():
        continue  # skip any non-directory files

    submission_name = submission_path.name
    output_dir = submission_path / "output"   # or "outputs", depending on your setup
    compose_file = submission_path / "docker-compose.yml"

    print(f"\n=== Evaluating submission: {submission_name} ===")

    # Step 1: Run the container if output is not already present
    if output_dir.exists() and any(output_dir.iterdir()):
        print(f"Output for {submission_name} already exists. Skipping container run.")
    else:
        # Ensure output directory exists
        output_dir.mkdir(exist_ok=True)
        # Run the Docker Compose up for this submission
        # Using detached mode (-d) so we can monitor it, then waiting for completion
        print(f"Running Docker container for {submission_name}...")
        subprocess.run(["docker-compose", "up", "-d"], cwd=submission_path)
        # Wait for the container to finish by polling its status
        # (This is a simple approach; in practice, you might check container logs or use docker SDK)
        container_id = subprocess.check_output(["docker-compose", "ps", "-q"], cwd=submission_path).decode().strip()
        if container_id:
            # Use docker wait to block until the container exits
            subprocess.run(["docker", "wait", container_id])
        else:
            print(f"Warning: No container ID found for {submission_name}. Proceeding without wait.")
        print(f"Container for {submission_name} has finished.")

    # Step 2: Calculate metrics by comparing outputs with ground truth
    if not output_dir.exists():
        print(f"Error: No output directory found for {submission_name}, skipping metrics calculation.")
        metrics = {}
    else:
        metrics = calculate_metrics(output_dir, GROUND_TRUTH_DIR)
        print(f"Metrics for {submission_name}: {metrics}")

    # Step 3: Log metrics to MLFlow (one run per submission)
    mlflow.start_run(run_name=submission_name)
    # Log a tag or parameter for identification
    mlflow.log_param("submission_name", submission_name)
    # Log each metric value
    for metric_name, metric_value in metrics.items():
        mlflow.log_metric(metric_name, metric_value)
    mlflow.end_run()

# After looping through submissions, you can stop here.
# The MLFlow UI will now contain an experiment with one run per submission, each with logged metrics.
print("\nEvaluation complete. Check the MLFlow UI for results.")
