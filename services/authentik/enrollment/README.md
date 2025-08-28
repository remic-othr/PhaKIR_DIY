#### Self-Registration with File Upload and Manual Approval in authentik
- **Create an Enrollment Flow:** Go to *Flows → Create*, type **Enrollment**.

- **Add a Prompt Stage:**  
   - Fields: `username`, `password`, `email`.  
   - Add a **File field** with key `attributes.verification_file` (required).
- **Optional: Email Verification Stage** Add before user creation if you want verified addresses.
- **User Write Stage:** - Enable *Create users as inactive*.
-**Finish Stage:** Add a static message: “Thank you. We will review your file and notify you.”
- **Admin Notifications** Configure under *Events → Notification Transports* (email/webhook) for “User created”.
- **Manual Review** (see [checkUser.py](./checkUser.py) )
   - Admin inspects `verification_file` in user attributes.  
   - If approved, activate the user and move them to target groups. 
   - Send a notification email.


**Note:** The file is stored Base64-encoded in user attributes. For large files, consider redirecting to an external upload backend and saving only a reference.