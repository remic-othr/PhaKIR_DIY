# Automated Evaluation with Docker and Python
One of the major advantages of a self-hosted challenge platform is the ability to run custom evaluation code on participants’ submissions. We automated the evaluation using Docker containers and Python scripts to ensure fairness and reproducibility.
## Evaluation Server Setup
It’s wise to separate the evaluation environment from the main web services server, especially if heavy computation or GPUs are involved. In our case, we had a dedicated GPU server that pulled the submissions and ran them. However, you can also use the same server if resources allow – just be cautious to allocate resources properly.

## Submission Format
We required participants to submit their algorithm encapsulated in a Docker container. This approach ensures that the code runs in an isolated, controlled environment and that all necessary dependencies are included. The container, when run, reads input data (the test images/videos) and outputs results in a predefined format (files in an output directory). We provided a template and testing tools so participants could adhere to this format. Using Docker guarantees that if the participant tested their container locally with our sample compose, it should run the same on our server.

> See the [PhaKIR Submission Template](https://github.com/remic-othr/PhaKIR_Submission_Template) for an example.

## Preparing Submissions
When a participant indicates they have submitted (for instance, by pushing to the Gitea registry or creating a release), the organizers (or an automated process) fetch the submission.

Therefore a docker-compose file is generated that pulls their Docker image from the Gitea registry.

> See the [PhaKIR Preparation Script](../Phakir/evaluation/Inferenz/prepare.py) for an example. Adapt the `docker-compose.yml.template` to fit your challenge boundaries, such as resource limits (CPU, memory, GPU) and the input/output directories.

This script can be run manually or by a webhook - using a continuous integration approach from Gitea - when a new submission is made.

> See the [PhaKIR CI Runner](../Phakir/evaluation/runner/) for an example.

**Alternative simple approach**: Have a cron job or loop that checks for new submissions every X
minutes via the Gitea API. - When found, download the Docker image. With Gitea’s registry, this is just a docker pull git.your-challenge.org/username/submission_repo:tag.

### Running the Containers
Manage your ressources!
Use your everyday GPU job queue or execute the `docker-compose up -d` for each participant directory consecutively with a script. Assuming each submission is in its own directory under `submissions/`, you can use the  
[PhaKIR Execution Script](../Phakir/evaluation/Inferenz/execute.py).

> [!WARNING] Dealing with Errors
> Currently there is no feedback to the participant during this process. They will not get informed if an error occurs. If the output directory stays empty, you should forward the dc.log file (e.g., email or Gitea issue) to the participant so they have to debug their submission.
We encountered issues where participants’ Docker containers failed (due to bugs, missing files, etc.) . Our solution during the challenge was to manually check the container logs and inform the team of the problem – a very timeconsuming process.

## Computing Metrics:
After the container finishes (it should exit on its own after processing), we have the participant’s outputs in the mounted output directory.
Next, you have to calculate the evaluation metrics based on these outputs. 

We strongly recommend using state of the art experiment tracking tools like [MLflow](https://mlflow.org/) to log your metrics and results. This allows you to track experiments, visualize results, and compare submissions easily.
Further, MLFlow allows you to share the leaderboard on your wordpress site.
> [!NOTE]  
> Keep in mind live leaderboards can motivate participants but also risk encouraging test data overfitting if used improperly. It’s a design choice.

We added an optional [MLflow server](/services/mlflow/) to our infrastructure, which can be used.

> See the [PhaKIR Evaluation Script](../Phakir/evaluation/Inferenz/evaluate.py) for an example of how to compute metrics from the outputs.

In the PhaKIR casestudy, we used a Python script that reads the output files and compares them to the ground truth data (the hidden test set) and logged the metrics manually.
This script will not be published, as it is tailored to the specific tasks of the PhaKIR challenge; you will implement whatever metrics are appropriate and produce scores. We took care to use standardized metrics definitions to ensure fairness.


## Finalizing Results
With evaluation done, your challenge winners are decided. Congratulations – the DIY challenge platform has run its course! 

