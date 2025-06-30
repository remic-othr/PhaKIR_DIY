# Participant Workflow: Registration to Submission
Understanding the end-to-end journey for a participant helps ensure our system components work
together smoothly. Here’s a typical workflow in our self-hosted challenge platform:
## Registration Phase
A potential participant visits the challenge website. They find a “Register”
link which redirects them to Authentik’s self-service registration page . The registration form
may ask for details like name, email, affiliation, and any required consent (e.g., agreeing to rules
or data usage terms). In our implementation, we even required participants to upload a signed
PDF agreement as part of registration , due to legal regulations on medical data. When the
participant submits the registration, their Authentik account is created but marked inactive/
pending.
## Account Approval
An organizer is notified (e.g., Authentik can send an email or one can
periodically check) that a new user registered. The organizer verifies the information (for us,
confirming the PDF was signed correctly) . Once everything is in order, the organizer
activates the account (this can be done in Authentik’s admin UI or via its API) . At this point,
the user is officially a participant with access credentials.

## Welcome and Onboarding
After activation, the participant can log in to the WordPress
challenge site (using the SSO login). They may now see additional content that was hidden
before – for example, a page with the dataset download link, the submission instructions, and
the discussion forum. It’s good to have a “Getting Started” page that appears for logged-in users,
guiding them on what to do next (download data, read instructions, join forum, etc.).

## Data Access
The participant proceeds to download the training data. If you used SFTP, the user
will use the same Authentik credentials – for instance, they might use an SFTP client with
username/password, or if Authentik issued SSH keys/cert, use that. If using Gokapi, they simply
click the download link provided (possibly entering a password if you set one). In our challenge,
data access was granted shortly after registration opened and account approval . Ensure you
communicate how to get the data clearly. If the dataset is large, recommend using a download
manager or provide checksums to verify integrity.

## Development Phase
Now the participant works offline, using the training data to develop their
algorithm or model. During this phase, they might need support – for example, clarifying data
format or handling edge cases. They can use the forum or issue tracker to ask questions, and
organizers should be responsive to ensure no one is blocked for long. It’s also wise to share any
baseline code to help participants get started (via the Gitea repo). Participants should also be
reminded of the timeline – e.g. how long they have until the submission deadline.

## Submission Preparation:
 As the submission deadline nears (or as participants finish their
method), they prepare their submission. In our blueprint, this meant building a Docker image
that can run their inference code. Participants used the provided template repository (on Gitea)
which included a Dockerfile and an example of how to structure input/output . They
would copy their model and inference script into this structure and test it locally (we provided a
docker-compose.yml to simulate the evaluation environment with resource limits ). This
step is critical – encourage participants to test their submission container with the provided tools
to catch errors early.

## Submitting Results/Model
The participant then submits according to your defined process:
If using Gitea for submissions: The participant could push their Docker image to the Gitea
registry. For example, tagging their image as git.your-challenge.org/username/
repo:submission1 and using Docker push (with Authentik credentials for authentication).
Alternatively, they might push code to a repository and notify organizers to build it. In our
challenge, we opted to have participants push to a Docker registry (to avoid transferring giant
models via git). Gitea served as the Docker registry and was integrated with Authentik for auth
. All submissions were recorded in the system, associated with the user’s account .
If using file upload: If you choose result file submission, then a participant might upload their
result files (e.g. a ZIP of output images or a CSV of predictions) through an upload portal or via
SFTP. You’d need to specify how they should name or structure these files. In such a case, when
they finish uploading, they might trigger a notification (like email or an issue on Gitea to tell you
it's ready).
It’s crucial to have clear submission guidelines published ahead of time (file formats, how many
submissions allowed, deadline date and time, etc.). Also consider whether you allow multiple
submissions and how you’ll pick the final one for scoring (some challenges let participants submit
several times but only the last or best counts).

## Automated Evaluation
Once a submission is in, the evaluation pipeline (described in the next
section) will run it on the hidden test set. Ideally, this is automated to run soon after submission
or all at once after the deadline. Participants might not get immediate feedback unless you
implement that. In our scenario, we did not provide a live leaderboard or immediate scoring –
final results were given after the challenge closed . However, you may choose to give partial
feedback or validation error messages (for instance, if a submission fails to run, you could
inform the team so they know there was an issue).
Challenge Conclusion: After evaluation, results are typically announced on the website and via
email. The WordPress site can display the leaderboard (which you manually input or generate
from the evaluation results). Accounts can be left active for a period or deactivated after the
challenge ends (we turned off access to services when the competition was over) . This is
to ensure no one can, for example, keep downloading data or push content after the fact. If you
plan future challenges, you might keep the Authentik accounts and just adjust permissions.
Throughout this timeline, having an admin checklist is useful. For example, when someone registers,
did they upload the agreement? Did we activate their account? When data is released, did we grant all
active users access? This ensures smooth operations.
The participant workflow above shows how the pieces come together: Authentik handles account
creation and login, WordPress is the info portal and entry point, data flows through MinIO to SFTP/
Gokapi to participants, development happens offline with support via forums or Gitea issues, and
submissions come back through Gitea (or upload) to be evaluated.


Next, we will detail the evaluation process implementation, which is the “hero moment” where
everything gets tested. &rarr; [Automated Evaluation with Docker and Python](./EVALUATION.md)
