
# Gokapi – Challenge Data Download Portal

[Gokapi](https://github.com/Forceu/Gokapi) is used in this infrastructure as a **lightweight, temporary download portal** to distribute datasets and resources to registered participants.

This service provides a simple way to:

- Share datasets (e.g. training/validation) with participants
- Distribute challenge-specific resources (e.g. FAQs, starter code)
- Replace email or SFTP-based distribution

Gokapi is browser-accessible and does **not require login**, but supports optional tokens/passwords for download protection.

---

## Setup

To run the service:

```bash
docker compose -f docker-compose.gokapi.yml up -d
```
Access its web console via Nginx Proxy Manager by creating a host like `download.example.org` forwarding to `gokapi:53842`.

Once running, access it via: `https://download.example.org/setup/`

Use the web interface to:
- Set expiry time (optional)
- Generate a download link with or without password/token

Recommentation:
- Use s3 garage storage for persistence, as described in the [Garage service documentation](../garage/).
Otherwise: If you want to use the default local storage, ensure the `gokapi` container has a volume mounted at `/data` to upload files.
- Use group based (admin) oauth authentication via Authentik to restrict access to the admin web UI.

## User Authentication via Authentik
Gokapi does not require user authentication by default, but you can secure it using Authentik outposts:
1. Set up a **Proxy Provider** in Authentik with:
   - Redirect URI: `https://download.example.org/outpost.goauthentik.io/*`
   - Group requirement: `users` (or any group you want to restrict access to)
2. Deploy an **Authentik Outpost** in front of Gokapi via NGINX.
3. Only authenticated users in the specified group can access the web UI.


## Role in the Infrastructure

- Participants receive links to download their respective resources.
- Uploads to Gokapi are managed by **Organizers only** via the web UI.
- Submissions happen **exclusively via Gitea** (Git push or Docker registry), not through Gokapi.

This separation ensures clear auditability and security for both directions of data flow.

---

### Security Notes

- Gokapi has **no user authentication**. Downloads can optionally be protected by passwords or tokens.
- **Reverse proxying via NGINX is required** – especially when using an [Authentik Outpost](https://docs.goauthentik.io/add-secure-apps/outposts/) to protect access.
- TLS termination (HTTPS) and routing are handled entirely via the proxy layer.

---

## References

- [Gokapi GitHub Repository](https://github.com/Forceu/Gokapi)
- [Official Gokapi Docker Image](https://hub.docker.com/r/forceu/gokapi)
