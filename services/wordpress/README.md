
# WordPress – Challenge Information Portal

[WordPress](https://wordpress.org/) is used in this infrastructure as a **flexible content management system (CMS)** to present and manage all publicly accessible challenge information.

It serves as the central **entry point** for participants, reviewers, and the broader research community and provides a structured and user-friendly way to:

- Present challenge details (goals, timeline, rules)
- Publish updates and news posts
- Embed tutorial content or videos
- Host a member area with extended materials (optional)
- Link to submission system, download portal, and documentation

> This aligns with the “Outward-Facing Services” layer described in the paper's infrastructure model.

## Setup
To run WordPress in this infrastructure, we use the official WordPress Docker image with a MySQL backend.
- Start the container via:
  ```bash
  docker compose -f docker-compose.wordpress.yml up -d
  ```
- Access its web console via Nginx Proxy Manager by creating a host like `challenge.example.org` forwarding to `wordpress:8000`.
- Access the site and follow the WordPress installation steps (set admin account, site name, etc.).

Single Sign-On (SSO) is implemented using:

- **OAuth** plugin for OAuth2
- **Authentik** as the identity provider

In Authentik:

- Create an OAuth2 provider with:
  - Redirect URI: `https://challenge.example.org/wp-login.php`
  - Scopes: `openid email profile`

Users are assigned roles based on group membership using the **Authentik WP Teams** plugin.

In WordPress:
- Install a suitable plugin (e.g. - [OpenID Connect Plugin](https://wordpress.org/plugins/daggerhart-openid-connect-generic/))  on WordPress, then configure it with Authentik’s details (similar to how we did for Gitea). 
- Configure the plugin with Authentik’s OAuth2 details:
  You’ll need the client ID/secret and endpoints from Authentik. Once set, your WordPress site will have a
  “Login” button that redirects to Authentik. You can choose to auto-create WordPress users upon first
  SSO login. We implemented secure OAuth2 login on our site so that only authenticated users
  (participants) could access certain pages.


## Role in the Infrastructure

According to the paper, WordPress functions as:

- The **core public entry point** of the challenge platform
- A flexible publishing platform for rules, metrics, and documentation
- An optional **communication hub** (e.g. with forum integration, FAQ pages, comments)

It separates communication tasks from submission logic and contributes to a modular, scalable design.

## Installed Plugins

The platform uses the following curated set of plugins:

- **Authentik WP Teams** – [Authentik-based user & team integration](https://github.com/schnadoslin/wp-authentik-teams)
- **OpenID Connect Generic** – OAuth2 login
- **Forminator** – Custom forms and surveys
- **wpForo** – Community forum support
- **Shortcodes Ultimate** – Visual building blocks
- **SiteOrigin Page Builder + Widgets** – Layout builder and dynamic content
- **Advanced Editor Tools** – Enhances block and classic editor
- **Block Visibility / If Menu** – Conditional content/menu rendering
- **WP Mail SMTP** – Email delivery via SMTP
- **Yoast SEO** – Search engine optimization
- **XCloner / All-in-One WP Migration** – Backup and restore
- **Sticky Menu**, **SVG Support**, **Duplicate Page**, etc. – Minor UI helpers

## References

- [WordPress.org](https://wordpress.org/)
- [OpenID Connect Plugin](https://wordpress.org/plugins/daggerhart-openid-connect-generic/)
- [Authentik OAuth2 Docs](https://docs.goauthentik.io/add-secure-apps/providers/oauth2/)
