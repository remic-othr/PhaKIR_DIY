
# Garage – S3-Compatible Object Storage

[Garage](https://garagehq.deuxfleurs.fr/) is used in this infrastructure as the central **S3-compatible storage layer**, offering unified and scalable file access for multiple services such as **Gitea**, **Gokapi**, and **CVAT**.

> In the PhaKIR challenge we originally relied on MinIO, but since the discontinuation of its open-source edition, **Garage** has become a strong and reliable alternative.

Garage runs as a Docker container, reverse-proxied via [NPM](/services/nginx-proxy/), and secured with SSO authentication for admin access through [Authentik](/services/authentik/).

### Key Features

- **High-performance object storage** with full S3 API compatibility  
- **Centralized management** of datasets, media, and submission archives  
- **Secure access control** leveraging OAuth2 integration with Authentik  
- **Open-source and actively maintained** by the Deuxfleurs collective  
---

## Setup

1) Generate secrets and paste them into the garage.toml.
Adjust your domains as needed.

```bash
cat > garage.toml <<EOF
metadata_dir = "/tmp/meta"
data_dir = "/tmp/data"
db_engine = "sqlite"

replication_factor = 1

rpc_bind_addr = "[::]:3901"
rpc_public_addr = "127.0.0.1:3901"
rpc_secret = "$(openssl rand -hex 32)"

[s3_api]
s3_region = "garage"
api_bind_addr = "[::]:3900"
root_domain = ".s3.garage.localhost"

[s3_web]
bind_addr = "[::]:3902"
root_domain = ".web.garage.localhost"
index = "index.html"

[k2v_api]
api_bind_addr = "[::]:3904"

[admin]
api_bind_addr = "[::]:3903"
admin_token = "$(openssl rand -base64 32)"
metrics_token = "$(openssl rand -base64 32)"
EOF
```

2) Start the container via:

```bash
docker compose -f docker-compose.garage.yml up -d
```

3) Now configure your garage:
```bash
# Rolle/Kapazität zuweisen
docker exec -it garag /garage layout assign -z dc1 -c 100G bd0f8597dc1588ce

# Layout anwenden (Version 1 beim ersten Mal)
docker exec -it garage /garage layout apply --version 1

# Prüfen
docker exec -it garage /garage status
docker exec -it garage /garage layout show
```

4) Create initial buckets for your your challenge data (e.g. gitea, gokapi, cvat-data) - [See the docs](https://garagehq.deuxfleurs.fr/documentation/quick-start/):

```bash
docker exec -it garage /garage bucket create gitea
docker exec -it garage /garage bucket create gokapi
docker exec -it garage /garage bucket create cvat-data
```

5) Secure the access via NPM by creating a host like `storage.your-challenge.org` following the [reverse proxy guide](https://garagehq.deuxfleurs.fr/documentation/cookbook/reverse-proxy/).

6) Optional: [Website for the bucket.](https://garagehq.deuxfleurs.fr/documentation/cookbook/exposing-websites/)

Garage is mainly for organizers’ use to manage and store data.

> The web UI should be restricted to members of the **“admin” group** in Authentik.

---


## Authentication via Authentik

To secure access for the Garage web UI, we integrate it with Authentik using an **Authentik Outpost**.:

1. Set up a **Proxy Provider** in Authentik with:
   - Redirect URI: `https://storage.example.org/outpost.goauthentik.io/*`
   - Group requirement: `admin`

2. Deploy an **Authentik Outpost** in front of Garage via NGINX

3. Only authenticated users in the `admin` group can access the web UI

---

## 🧩 Integrations

### a) Gitea – Object Storage for Attachments and CI

In `app.ini`:

```ini
[storage]
STORAGE_TYPE = minio
MINIO_ENDPOINT = garage:3900
MINIO_ACCESS_KEY_ID = your_access_key
MINIO_SECRET_ACCESS_KEY = your_secret_key
MINIO_BUCKET = gitea
MINIO_LOCATION = us-east-1
MINIO_USE_SSL = false
SERVE_DIRECT = true 
```

### b) Gokapi – Upload Backend

In Gokapi `.env` file:

```env
STORAGE_DRIVER=s3
S3_ENDPOINT=http://garage:3900
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
CVAT_S3_ENDPOINT=garage:3900
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

- [Garage Documentation](https://garagehq.deuxfleurs.fr/documentation/quick-start/)
- [Authentik Outpost Setup](https://docs.goauthentik.io/add-secure-apps/outposts/)
