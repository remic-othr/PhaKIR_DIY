# LimeSurvey - An open source survey tool


[LimeSurvey](https://github.com/LimeSurvey/LimeSurvey) is a powerful open-source survey tool that can be used to create and manage online surveys. It is particularly useful for gathering feedback from challenge participants, reviewers, and other stakeholders.

## Key Features
- **Customizable Surveys**: Create surveys with a wide range of question types, including multiple-choice, open-ended, and rating scales.
- **Conditional Logic**: Implement skip logic and branching to tailor the survey experience based on participant responses.
- **Data Export**: Export survey results in various formats (CSV, Excel, SPSS) for further analysis.

>[!Tip] [Have a look at our survey!](/PhaKIR/survey)

## Setup
To run LimeSurvey in this infrastructure, we use the official LimeSurvey Docker image with a MySQL backend.
- Start the container via:
  ```bash
  docker compose -f docker-compose.limesurvey.yml up -d
  ```
- Access its web console via Nginx Proxy Manager by creating a host like `survey.example.org/admin` forwarding to `limesurvey-app:8080`.

- To go with your Single Sign-On (SSO) using Authentik, you can use
the [OpenID Plugin](https://github.com/Worteks/AuthOpenIDConnect) for limesurvey.
