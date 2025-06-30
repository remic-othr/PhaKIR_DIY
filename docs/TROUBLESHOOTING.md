# Troubleshooting Tips:
DNS and Domain Issues: If your subdomains aren’t reachable, verify the DNS records and ensure they’ve propagated. A common hiccup is forgetting to add DNS records for new subdomains or typos in names. Tools like nslookup or online DNS checkers help confirm your domain is correctly configured to point at your server. 
## Nginx Proxy Manager Problems
If you don’t get the NPM admin interface on port 81, check the Docker logs for errors (perhaps port conflicts). If a proxy host isn’t working (e.g., you get a bad gateway), ensure the target container is up and that you used the correct internal host/port. For LetsEncrypt SSL issues, make sure port 80 is open and not blocked by a firewall, and your domain is pointing correctly (HTTP validation needs to reach your NPM).
## Authentik Integration
A frequent problem is OAuth callback URLs mismatch. If login isn’t working, double-check that the redirect URI in Authentik’s provider config exactly matches what the client (Gitea/
WP) is using, including http/https and trailing slashes. Authentik’s logs (accessible via its admin UI or docker logs) can be helpful – they might show why a login attempt failed. Also ensure the time on your server is correct (OAuth tokens can fail if time is off significantly).
## Gitea Issues
If SSO is set up but users can’t login, confirm the Authentik provider in Gitea is enabled and try a test with a fresh Incognito browser to rule out any session issues. If repositories or Git LFS are large, Gitea might need increased
limits (configure max file size in app.ini). For any performance issues, consider giving Gitea more memory or switching to an external database rather than SQLite.
## Data Transfer Snags
For SFTP, users might face firewall issues on their side (SSH port 22 blocked). In such cases, having an HTTPSbased method (like Gokapi) as fallback helps. If using Gokapi and downloads are failing, check container logs – maybe the link expired or password was wrong.
## CVAT Quirks
CVAT can be resource-intensive; if it’s slow or unresponsive, ensure the server has enough CPU/RAM when many images are loaded.
Sometimes a restart of CVAT containers can solve weird bugs. Always export your annotations periodically so you don’t lose work if something happens.
## Docker Evaluation
If a participant’s container hangs or never exits, you’ll have to decide on a timeout (you can use Docker’s --timeout or
handle it in your script by killing after X minutes). Monitor system usage; if one container is using too much (beyond expected limits), you might have to abort it. Check logs for errors – if a container fails immediately (bad command, etc.), share that log with the participant if there’s still time for them to fix and resubmit. During the final evaluation, if something fails and time is over, you might have to give
that submission a score of 0 or handle it per your rules.
## Lessons Learned and Future Improvements
### Automate Early, Test Often
One key lesson we learned was to automate the submission verification process. Some participants did not follow the submission instructions correctly, leading to broken Docker containers. We spent a lot of time
manually reviewing logs and guiding them. In the future, integrating an automated pre-check (e.g., a CI pipeline that tries to run each container on a small sample) would save a huge amount of time and catch errors before the deadline. We highly recommend building a “submission validator” and making it available to participants (so they can self-check) and using it as an entry filter. 
### Consider Live Leaderboards
Participants appreciate timely feedback. We initially planned only a final evaluation, but
some requested a live ranking during the challenge. Implementing a public leaderboard that updates (either continuously or at certain intervals) can increase engagement. If doing so, one way is to have the evaluation script push scores to MLFlow that can be embedded intop the WordPress site. This needs careful handling to avoid revealing too much (you might show ranks or partial info to avoid overfitting to the test set).
### Scalability
Our framework was modular and could handle the
participants we had, but if your challenge scales to hundreds of participants, be mindful of load: 
- The reverse proxy can handle many connections, but ensure the server bandwidth is high. 
- Authentik and WordPress can handle many users logging in, but test the login flow under load if possible.
- Gitea might need tuning (number of Git operations, enabling CDN for large file downloads, etc.) for large
numbers of repos or users simultaneously.
- For evaluation, if you expect many submissions at once,
plan for parallelism (maybe multiple evaluator containers running concurrently, if you have the CPU/
GPU resources).
- Team Management: If teams are allowed, think about how you handle team registration. We used a WordPress plugin for team self-organization . Alternatively, you could require one person to register and then email you team member names. This can get complicated with Authentik accounts for each member. Our approach let each member register individually (so each had an account) but then they joined a team entity on the site for tracking. Choose whatever is simplest for you, but ensure clarity in rules about teams vs individual entries.
### Post-Challenge Transition
Once the challenge is over, it’s good to archive everything. We deactivated service access after conclusion . You might convert the WordPress site to a static page (for long-term availability of results) or keep it running
for a while. 
- Gather feedback from participants – we attempted a post-challenge survey , though we had a low response rate. Even with few responses, you can learn what participants liked or struggled with. In our case, the feedback highlighted strengths of the DIY platform and areas to refine, validating that a self-hosted approach is viable and appreciated by the community .
