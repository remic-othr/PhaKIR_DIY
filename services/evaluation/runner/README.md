# PhaKIR CI Runner (Minimal Setup)

This folder provides a minimal configuration for running a Gitea CI runner with Docker.  

It is meant as a starting point for connecting your own runner to the PhaKIR submission platform.


## What is included

- `docker-compose.yml` – starts a `gitea/act\_runner` container  

- `config.yaml` – basic runner configuration (logging, network, working directory)  

- `.env` – holds your runner registration token (must be filled before starting)  



## How to use

1. Copy the provided `.env` file and insert your registration token.  

2. Start the runner with:  



&nbsp;  ```bash

&nbsp;  docker compose up -d

&nbsp;  ```  


3. The runner will register with the PhaKIR Gitea instance and wait for jobs.

## Important

- This is only a **minimal runner setup**.  

- You still need to define your own workflows in the corresponding repositories (e.g. what should happen when new submissions arrive).  

- Keep your `.env` file private; do not commit your token.


## Further Reading

- [**Official Gitea documentation – Act Runner**](https://docs.gitea.com/usage/actions/act-runner)

&nbsp; Covers Docker setup, registration, ephemeral runners, daemon mode.


- [**vegardit/docker-gitea-act-runner**](https://github.com/vegardit/docker-gitea-act-runner)

&nbsp; Prebuilt Docker images for act_runner including DooD and DinD variants.



