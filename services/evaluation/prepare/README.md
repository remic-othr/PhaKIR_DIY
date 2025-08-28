# PhaKIR Evaluation Helper

This folder contains the helper script and template for preparing the local evaluation environment.

## Files
- `prepare.py` — queries the submission registry, pulls Docker images, and creates the local folder structure.
- `docker-compose.yml.template` — base template for generating team-specific compose files.
- `.env.sample` — example configuration for registry URL, user, and password.

## Usage
1. Copy `.env.sample` to `.env` and fill in your credentials.  
2. Make sure Python (with `requests` and `python-dotenv`) and Docker are installed.  
3. Run:
   ```bash
   python prepare.py --root ./phakir
