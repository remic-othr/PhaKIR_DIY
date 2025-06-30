
# Security Considerations for a Self-Hosted Challenge Platform

Setting up multiple services and managing user submissions inherently comes with security and operational challenges. This section provides guidance on keeping the platform secure, advice on troubleshooting common issues, and insights from our own experience (things we’d improve or do differently in future).

## Security Best Practices

### Network Security
By using Nginx Proxy Manager with HTTPS, all user interactions with the platform are encrypted . Always obtain SSL certificates (LetsEncrypt) for your domains. If your server is on a university network, coordinate with IT for any firewall openings.
Close all unnecessary ports on the server (only expose what’s needed: 80/443 for NPM, maybe 22 for SSH admin access, and high ports if you didn’t proxy them).
### Centralized Authentication
Authentik is a security-focused, open-source Identity Provider (IdP) supporting modern authentication protocols such as OAuth2/OIDC (including PKCE, refresh tokens, JWT encryption), SAML, and LDAP, as well as multi-factor methods like TOTP and WebAuthn/Passkeys. It enables fine-grained access control via configurable flows, stages, and policies, with context-aware conditions (e.g., GeoIP, device, time-based rules). Security features include brute-force protection, CAPTCHA stages, session binding, redirect URI validation, and short-lived tokens. Detailed audit logs with field-level tracking ensure full traceability. For secure deployment, best practices include reverse proxy hardening with Content Security Policy (CSP), mutual TLS (mTLS) for admin endpoints, strong passwords, MFA for admins, and regular updates. Authentik offers forward-auth and app proxying to secure legacy applications, undergoes regular security reviews (including CVEs), and follows a transparent release and disclosure process. When properly hardened, Authentik is safe for public exposure.

### Principle of Least Privilege
Give users access only to what they need. For instance, participants shouldn’t see each other’s private repos or submissions. Use Gitea’s permissions to enforce this. On data download, require registration and agreement to terms before granting access – this adds a layer of accountability. In
our setup, accounts were only activated after they agreed to rules and were individually approved
### Isolate Evaluation Environment
Treat submitted code as untrusted. Our evaluation was done in
a “protected Docker environment” – meaning containers ran with no network and limited resources. You can even run them as a non-root user inside the container (e.g., have Dockerfile use a user). If you use a shared GPU server, consider using Linux user namespaces or Docker’s --user flag so that containers don’t run as root on the host. Monitor the evaluation process – if something tries to break out or consume too much, you can kill it. Tools like Docker resource limits, AppArmor profiles, or
Kubernetes with strict policies can help contain potential malicious behavior.
### Data Protection
If working with sensitive medical data, keep all data storage (MinIO, volumes, databases) secure. That might involve disk encryption at rest, though on a server in a secure facility this may be optional. The biggest risk is data leakage via the platform, which we mitigated by requiring logins for data access and by auditing who downloaded what (SFTP logs, etc.). Also, after the challenge, ensure that data access is revoked (e.g., disable those accounts or remove files from the download area).
### Web Application
Keep your WordPress and plugins updated to the latest versions, as WordPress can be a target for attacks. Only install necessary plugins and choose well-maintained ones (since outdated
plugins are a common breach point). Similarly, update all Docker containers periodically (especially those facing the internet like Nginx Proxy Manager, Authentik, etc.) to get security fixes.
### Backups
Regularly backup critical data: the database of WordPress, the Authentik database (which has user accounts), Gitea repositories (and any registry storage), and your MinIO data. This is crucial in case of server failure or if a mistake is made (e.g., someone accidentally deletes a repo). Automated daily or weekly backups to a secure offsite location would be ideal.
