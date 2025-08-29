
# Authentik – Identity and Access Management for DIY Challenges

**Authentik** is a contemporary identity and access management (IAM) system built on open standards such as OAuth2 and OpenID Connect (OIDC). In the context of a biomedical image analysis challenge, Authentik enables:

- **Single Sign-On (SSO)**: Participants, organizers, and admins sign in centrally to access all services (Gitea, WordPress, SFTP, CVAT, MinIO).
- **Granular Role-Based Access Control (RBAC)**: Define precise permissions ensuring participants and organizers access only authorized resources.
- **Self-Service User Management**: Streamlined user registration and approval flows, enhancing administrative efficiency.
- **Audit and GDPR Compliance**: Centralized logging and management of user actions to facilitate compliance with data protection regulations.
- **Seamless Integration**: Easily integrates with widely-used services like Gitea, WordPress, and CVAT via standard OAuth2 interfaces.

---

Based on the stakeholder roles described in the paper, we suggest the following role structure within Authentik:

| Role            | Description                                | Example Permissions                                           |
|-----------------|--------------------------------------------|---------------------------------------------------------------|
| **Admin**       | Infrastructure management, full access     | User management, service integrations, audit logging          |
| **Organizer**   | Challenge and submission management        | Approving users, uploading datasets, managing submissions     |
| **Participant** | Access to own submissions and data         | Data download, submission uploads                             |
| **Data Provider** | Creation and management of annotations | Access to CVAT, annotation creation, quality control          |

>[!NOTE]
> See detailed "Stakeholder-Roles" in the paper (section 2.1).

---

## Setup 

### Step 1: Install latest Authentik Docker Compose Setup

The latest Authentik version can be set up using Docker Compose. Follow the official documentation for installation:
[Docker Compose Setup](https://docs.goauthentik.io/docs/install-config/install/docker-compose/)

Otherwise you can use the provided `docker-compose.authentik.yml` file in this repository. This file is pre-configured for our nginx proxy setup and has all configurations in the env file.

- Fill the env file with your values and secrets and rename it (`authentik.env.template` to `authentik.env`).
- Start Authentik with the following command:
  ```bash
  docker compose -f docker-compose.authentik.yml up -d
  ```

### Step 2: Configure your Nginx Proxy Manager (NPM)

Follow the documentation to set up Nginx Proxy Manager:

- [**Nginx Proxy Manager Installation Guide**](../nginx-proxy/README.md)

After setting up Nginx Proxy Manager, configure a new proxy host for Authentik via the GUI.

- **Domain**: e.g. `auth.example.org`
- **Forward IP / Port**: `authentik:9000` (check the container name of the authentik server with `docker ps`)
- **Scheme**: `http`
- Enable **SSL** (Let’s Encrypt), **Force SSL**, and **HTTP/2**
- Enable **Websockets**!.

Your Authentik instance is now securely available via HTTPS through Nginx Proxy Manager.

### Step3: Initialization
- Access `https://auth.example.org/if/flow/initial-setup/`. The setup wizard will prompt you to create an
admin user.
- Enable email settings if you want Authentik to send verification emails (configure SMTP).
- Consider enabling selfservice registration so participants can sign up on their own. Authentik supports flexible user flows – in
our case, we allowed self-registration but with a manual approval step (more on that in the workflow section).
> [!TIP]
> Take your time to explore Authentik’s documentation and features. It's worth understanding the concept.

### Step 4: Define Roles and Groups
Authentik will be the source of truth for user identities. 
- You can define groups or roles in Authentik (e.g. “participants”, “organizers”) to manage permissions.
For instance, you might only allow verified participants to access certain resources (data downloads, submissions).

Authentik’s advantage is that one account’s permissions can propagate across services. In our challenge
setup, Authentik was used for all services except perhaps the data collection interface . Centralizing
authentication makes it easier to deactivate a user’s access entirely at the end of the challenge or if
issues arise.

Tip: Make use of Authentik’s security features like password policies and multi-factor authentication
for admin accounts. Also generate a strong secret key for Authentik. With Authentik in place, we have a
secure IAM foundation for the challenge platform.

### Step 5: User Registration and Approval Workflow

>[!TIP]
>Instead of taking care of user authentikcation you can use common provicders like Github for authentication if you like so. This is supported by Authentik.

- Activate self-service registration.
- Define an admin approval flow for manual validation after receiving signed user agreements (Data Agreements).
Have a look how we implented the [enrollment](./enrollment/).

### Step 6: Integrate Authentik with Platform Services

We will use Authentik as the OAuth2 provider for our other services:
- WordPress: Use an [WordPress OAuth Plugin](https://wordpress.org/plugins/daggerhart-openid-connect-generic/) on WordPress to delegate login to Authentik.
- [Gitea](https://docs.gitea.com/development/oauth2-provider): Gitea has built-in OAuth2/OIDC authentication; we’ll register Authentik as a provider.
- Others
(optional): If possible, integrate CVAT and other tools with SSO: [CVAT OIDC](https://docs.cvat.ai/docs/enterprise/sso/#auth0)
 If a service doesn’t support external auth, Authentik can protect it via a proxy (Authentik has an embedded outpost feature to act as a forward-auth agent).

To set up an OAuth app in Authentik for a service, you typically do the following in Authentik: 
1. Create an Application (representing the service, e.g. "Gitea") with a Client ID and Client Secret.
2. Create a Provider of type OAuth2/OIDC, link it to the Application, and set redirect URLs to the service’s callback URL (e.g. for Gitea, https://git.your-challenge.org/user/oauth2/authentik/callback ).
3. Configure the service (e.g. in Gitea’s config or WP plugin settings) with the Authentik OAuth endpoints
and the Client ID/Secret.

For example, to integrate Gitea with Authentik: in Authentik create an OAuth2 provider for Gitea, and in
Gitea’s configuration ( app.ini or admin settings), add Authentik as an OAuth2 authentication source
with the authorization URL ( https://auth.your-challenge.org/application/o/authorize/ ),
token URL, and user info URL provided by Authentik. Once set up, users visiting Gitea will be
redirected to Authentik to log in. Similarly, for WordPress, install a plugin such as “OAuth Single Sign On
(OIDC)” and configure Authentik as the OIDC provider (client ID/secret, endpoints). This will allow a
“Login via Authentik” button on the WP site and SSO login.

### Step 7: Legal Compliance
- Ensure users agree to the challenge rules and data usage terms during registration.

Have a look at our [additional documents](/PhaKIR/).

---



## References


| Topic                          | Documentation Link                                    |
|--------------------------------|-------------------------------------------------------|
| **Authentik Documentation**    | [Authentik Docs](https://docs.goauthentik.io/)        |
| **Docker Compose Example**     | [Docker Compose Setup](https://docs.goauthentik.io/install-config/install/docker-compose/) |
| **OAuth2 Provider**            | [OAuth2 Provider Guide](https://docs.goauthentik.io/add-secure-apps/providers/oauth2/) |
| **Flows and Policies**         | [Authentik Flows](https://docs.goauthentik.io/add-secure-apps/flows-stages/flow/) |

---

## GDPR and Security Compliance

- **Minimize stored user data**: Only collect essential user information (e.g., name, email).
- **Restrict data access**: Limit user data visibility strictly to necessary roles.
- **Explicit Consent**: Users must actively consent to data and usage terms.
- **Audit Logging**: Maintain comprehensive logs of user activities for auditing purposes.

>[!NOTE]
> See especially "Infrastructure Requirements" and "IAM Lifecycle" in the paper for further details.


