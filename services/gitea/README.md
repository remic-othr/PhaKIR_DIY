
# 🧪 Gitea – Submission System for Challenge Participants

[Gitea](https://gitea.io/) serves as the primary **submission interface** for participants in the PhaKIR Challenge infrastructure.

In our case study it is used for submitting **Docker containers** via the internal container registry, with image tags used to indicate specific **challenge tasks**.

- Participants push Docker images (via tag) to Gitea's internal registry.
- Tags define the **task identifier** the submission refers to.
- A webhook triggers the evaluation pipeline once a new image is received.
- Gitea stores code repositories and artifacts in **MinIO** (S3) storage.


## Setup
- To run the service, fill out the `gitea.env.template` file with your settings and secrets, then rename it to `gitea.env`.
- Start the container via:
   ```bash
   docker compose -f docker-compose.gitea.yml up -d
   ```
- Access its web console via Nginx Proxy Manager by creating a host like `submit.example.org` forwarding to `gitea:3000`.

On first accessing Gitea’s web UI, you’ll go through an install wizard (if not preconfigured). Use the wizard to finalize settings: database (if using SQLite it’s auto), repository root path (default is fine), and the OAuth2 provider info for integration with Authentik. Gitea will ask for OAuth settings if you want to allow login via an external provider. We will set that up now.

**SSO Integration**: In Authentik, as mentioned, create an OAuth2 app for Gitea. In Gitea’s configuration,
add Authentik as an OAuth2 source (Gitea’s docs or UI will have fields for the provider’s name, client ID,
secret, auth URL, token URL, etc.). After configuring, Gitea’s login page will show an option to “Login
with Authentik”. This means participants will use their Authentik account to access Gitea, and you
don’t need to separately manage Gitea accounts.

After Gitea is integrated with **Authentik** via OAuth2 SSO, participants should be grouped via roles such as:
- `submitter` – Can push to submission repo
- `admin` – Full platform access
- `reviewer` – Read-only access to all repos
Access is enforced using group membership within Authentik.


## Docker-Based Submissions

> Have a look at the [PhaKIR Submission guides](https://github.com/remic-othr/PhaKIR_Submission_Template).

## Object Storage Integration

All uploaded files and attachments are stored via MinIO (S3):

```ini
[storage]
STORAGE_TYPE = minio
MINIO_ENDPOINT = storage:9000
MINIO_ACCESS_KEY_ID = your_access_key
MINIO_SECRET_ACCESS_KEY = your_secret_key
MINIO_BUCKET = gitea
MINIO_LOCATION = us-east-1
MINIO_USE_SSL = false
```

This ensures separation of repository data and persistent object storage.

## Automation

Webhooks are configured in Gitea to notify the evaluation engine of new pushes:

- Event: `push`
- Target: Internal webhook endpoint
- Payload: Contains repository, tag, user info

These triggers execute:
- Image download and container execution
- Task-specific metric evaluation
- Result recording and feedback

## Role in the Infrastructure

As defined in the infrastructure blueprint, Gitea:

- Provides a **lightweight, self-hosted DevOps interface** for challenge evaluation
- Replaces ad-hoc FTP/email submissions
- Integrates tightly with evaluation, storage and identity services

## References

- [Gitea Docs](https://docs.gitea.io/)
- [Gitea Docker Registry](https://docs.gitea.io/en-us/packages/#docker-container-registry)
- [Authentik OAuth2 Setup](https://goauthentik.io/docs/providers/oauth2/)
- [PhaKIR Infrastructure Paper](https://doi.org/10.1007/978-3-031-49977-2_21)
