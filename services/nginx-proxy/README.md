
# 🧭 NGINX Proxy Manager (NPM)

This service acts as the central reverse proxy and TLS termination point for the entire DIY Challenge infrastructure.
It allows incoming HTTPS traffic to be routed to internal services like:
- [Authentik (Identity Management)](../authentik/)
- [Gitea (Submissions)](../gitea/)
- [WordPress (Information Portal)](../wordpress/)
- [CVAT (Annotation Tool)](../cvat/)
- [Gokapi (Data Access)](../gokapi/)


Nginx Proxy Manager simplifies routing and SSL so you don’t have to configure Nginx
from scratch. It supports features like access lists and HTTP authentication if needed. In our setup, the
reverse proxy acts as a central gateway to all services, enhancing security and ease of access .
You can later integrate the proxy with the SSO (Authentik) for additional access control, but initially, the
proxy will just ensure all services are reachable at nice URLs with HTTPS.

## Setup

We use [NGINX Proxy Manager](https://nginxproxymanager.com/) in its official Docker container variant.

To get started, use the included `docker-compose.nginx.yml`. 

Start the proxy with:

```bash
docker compose -f docker-compose.nginx.yml up -d
```

Access the NPM management UI at `http://<your-server-ip>:81` and log in (default credentials are usually admin@example.com /
changeme ; you will be prompted to change them). From the dashboard, you can start adding Proxy
Host entries for each service in your platform.
Start with an Entry for your NPM instance itself (`http://localhost:8181`)

#### Configure Proxy Hosts and SSL:
Nginx would be fully automatable, but it does not have a web GUI. 
Nginx Proxy Manager (NPM) is GUI-first with convenience, SSL handling, and easy forwarding. This makes it easier for non-DevOps experts to add new modules. Therefore, all services must be entered manually.

For each service (Authentik, MinIO, CVAT, Gitea, WordPress, etc.), decide on a subdomain and the internal port it’s running on.

1. Create a new **Proxy Host**:
   - Domain: `auth.example.org`
   - Forward Hostname/IP: internal service name (e.g., `authentik`)
   - Port: e.g., `9000` for Authentik
   - Scheme: `http`
2. Enable **SSL**:
   - Request Let's Encrypt Certificate
   - Enable **Force SSL** and **HTTP/2**
3. Optinal:  Enable Websockets if the service needs it (e.g. some apps like CVAT might use websockets).
3. Save

Repeat for all services. Make sure the NPM container can resolve the internal service names via Docker network.

NPM will automatically perform the ACME challenge and fetch a certificate for your domain. Ensure port 80 is
accessible for the HTTP challenge. Once added, NPM will route HTTPS traffic for that subdomain to the
service, securing all traffic with SSL.

## Role in the Infrastructure

As described in the paper, this component enables:

- Secure user access to internal services via a unified domain space
- Easy certificate management via Let's Encrypt
- Separation between public access and sensitive backend logic (e.g. evaluation)

NPM contributes to the **privacy-aware, modular and compliant infrastructure** emphasized in our DIY approach to challenge organization.

---

## References

- [Official Docs](https://nginxproxymanager.com/)
- [Compose Setup Reference](https://nginxproxymanager.com/guide/#quick-setup)
