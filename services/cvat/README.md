
# 🖍️ CVAT – Computer Vision Annotation Tool

[CVAT](https://github.com/opencv/cvat) is used as the official annotation platform for this challenge infrastructure. It enables **collaborative labeling of images and videos** and supports both manual and semi-automated annotation workflows.

This service is used primarily by **data providers** and **organizers** to:

- Annotate raw challenge data (e.g. bounding boxes, masks, keypoints)
- Validate or revise participant submissions (optional)
- Prepare gold standard datasets

## Setup

- Fill out the `cvat.env.template` file with your settings and secrets, then rename it to `cvat.env`.

- Start the container via:

    ```bash
    docker compose -f docker-compose.cvat.yml up -d
    ```
- Access its web console via Nginx Proxy Manager by creating a host like `cvat.example.org` forwarding to `cvat:8080`.


CVAT supports **OIDC/OAuth2 login**, and is integrated into this infrastructure using **Authentik** as identity provider.
- Redirect URI: `https://cvat.example.org/auth/cvat/login/callback`
- Client Type: `confidential`
- Scopes: `openid email profile`
- Set environment variables or mount a pre-configured `cvat.env` file if needed.

> Participants and annotators log in via the Authentik SSO flow and are assigned roles based on group membership.

Alternatively, you can use the built-in local authentication, but this is not recommended for production use.

## Usage
Create a new annotation project for your dataset. CVAT can import images or connect to
cloud storage. If your data is in MinIO, you might either download it and upload to CVAT or mount a
volume. CVAT supports sharing tasks among annotators and reviewing annotations. In our case study, a
dedicated CVAT instance was provided to medical partners to coordinate ground truth creation, which
improved consistency of labels. You can track progress and ensure multiple experts cross-verify
some annotations to maintain quality (medical data often benefits from consensus labeling due to
inter-observer variability).

## Role in the Infrastructure

- Access is restricted to **authorized users** (e.g. Organizers or Data Providers).
- Supports human-in-the-loop tasks such as annotation refinement.
- Task definitions and outputs can be exported in COCO, VOC, and custom formats.
- Annotations can be re-used to generate evaluation labels or training data.


## References

- [CVAT GitHub Repository](https://github.com/opencv/cvat)
- [CVAT OAuth2 Configuration](https://opencv.github.io/cvat/docs/administration/advanced/oidc/)
- [Authentik OAuth2 Provider Setup](https://goauthentik.io/docs/providers/oauth2/)
- [PhaKIR Infrastructure Paper](https://doi.org/10.1007/978-3-031-49977-2_21)
