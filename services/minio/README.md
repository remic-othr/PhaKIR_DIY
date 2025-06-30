
# 🗃️ MinIO – S3-Compatible Object Storage

[MinIO](https://github.com/minio/minio) is used in this infrastructure as the central **S3-compatible storage layer**, providing unified and scalable file access for several services including Gitea, Gokapi, and CVAT.

It runs as a Docker container, reverse-proxied through NGINX, and secured via **SSO authentication for admin access only** using **Authentik**.

MinIO provides:

- High-performance object storage with S3 API compatibility
- Centralized management of data assets (datasets, media, submission archives)
- Secure access control via OAuth2 / Authentik

---

## Setup

Start the container via:

```bash
docker compose -f docker-compose.minio.yml up -d
```
Access its web console via Nginx Proxy Manager by creating a host like `storage.your-challenge.org` forwarding to `minio:9001`

- Log in with the MINIO_ROOT_USER/PASSWORD.
- Create a bucket for your challenge data (e.g. challenge-dataset ).
- Set up CORS rules if needed (e.g. for CVAT or Gokapi to access MinIO).

You can upload files via the web UI or use the mc command-line tool. MinIO provides a web interface
for file management and an S3 API for programmatic access.

MinIO is mainly for organizers’ use to manage and store data.

> The web UI should be restricted to members of the **“admin” group** in Authentik.

---


## Authentication via Authentik

To secure access:

1. Set up a **Proxy Provider** in Authentik with:
   - Redirect URI: `https://storage.example.org/outpost.goauthentik.io/*`
   - Group requirement: `admin`

2. Deploy an **Authentik Outpost** in front of MinIO via NGINX

3. Only authenticated users in the `admin` group can access the web UI

---

## 🧩 Integrations

### a) Gitea – Object Storage for Attachments and CI

In `app.ini`:

```ini
[storage]
STORAGE_TYPE = minio
MINIO_ENDPOINT = minio:9000
MINIO_ACCESS_KEY_ID = your_access_key
MINIO_SECRET_ACCESS_KEY = your_secret_key
MINIO_BUCKET = gitea
MINIO_LOCATION = us-east-1
MINIO_USE_SSL = false
```

### b) Gokapi – Upload Backend

In Gokapi `.env` file:

```env
STORAGE_DRIVER=s3
S3_ENDPOINT=http://minio:9000
S3_BUCKET=gokapi
S3_REGION=us-east-1
S3_ACCESS_KEY=your_access_key
S3_SECRET_KEY=your_secret_key
S3_FORCE_PATH_STYLE=true
```

> Set correct CORS rules and policies for the `gokapi` bucket.

### c) CVAT – Media and Annotation Backup

In CVAT environment config:

```env
CVAT_S3_ENDPOINT=minio:9000
CVAT_S3_USE_SSL=False
CVAT_S3_ACCESS_KEY_ID=your_access_key
CVAT_S3_SECRET_ACCESS_KEY=your_secret_key
CVAT_S3_BUCKET=cvat-data
CVAT_S3_REGION=us-east-1
```

---

## Configuration Notes

- All services access MinIO via internal Docker networking (`minio:9000`)
- The MinIO web UI is only available via NGINX proxy (`https://storage.example.org`)
- Authentik restricts access to trusted users with admin privileges

---

## References

- [MinIO Documentation](https://min.io/docs/)
- [Authentik Proxy Setup](https://goauthentik.io/docs/providers/proxy/)
- [S3 CORS Configuration](https://docs.min.io/docs/minio-server-cors-support.html)
- [PhaKIR Challenge Infrastructure Paper](https://doi.org/10.1007/978-3-031-49977-2_21)
