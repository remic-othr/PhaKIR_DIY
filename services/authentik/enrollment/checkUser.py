import requests
import time
import base64
import io
from PIL import Image
from pdf2image import convert_from_bytes
import smtplib
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from dotenv import load_dotenv
import os

# load .env file into environment
load_dotenv()

def send_mail(to_address, html_content):
    # SMTP server configuration
    smtp_server = os.getenv("SMTP_SERVER")
    smtp_port = int(os.getenv("SMTP_PORT"))
    smtp_username = os.getenv("SMTP_USERNAME")
    smtp_password = os.getenv("SMTP_PASSWORD")

    # Create a multipart message
    message = MIMEMultipart("alternative")
    message["Subject"] = "Confirmation of your registration in the Phakir platform"
    message["From"] = os.getenv("MAIL_ADDRESS")
    message["To"] = to_address

    # Create HTML content
    html_part = MIMEText(html_content, "html")

    # Attach HTML part to the message
    message.attach(html_part)

    try:
        # Connect to the SMTP server
        with smtplib.SMTP_SSL(smtp_server, smtp_port) as server:
            # Login to the SMTP server
            server.login(smtp_username, smtp_password)
            # Send the email
            server.sendmail(smtp_username, to_address,  message.as_string())
        print("Email sent successfully!")
    except Exception as e:
        print("Failed to send email:", str(e))
        


url_base = f"{os.getenv('AUTH_BASE_URL').rstrip('/')}/api/v3/"
headers = {
    "Authorization": f"Bearer {os.getenv('AUTH_TOKEN')}"
    }

users=[]
group_url = url_base + "core/groups/"
response = requests.get(group_url, headers=headers, params={"name": os.getenv("AUTHENTIK_GROUP") })
userIds = []
if response.status_code == 200:
    data = response.json()
    # Process the response data here
    for group in data["results"]:
        if group["name"] == os.getenv("AUTHENTIK_GROUP") :
                users = [user_obj for user_obj in group["users_obj"]]       
    users = [user for user in users if not user["is_active"]]
else:
    print("Request failed with status code:", response.status_code)

print(f"Possible candidates in the {os.getenv('AUTHENTIK_GROUP')} are", ([u["username"] for u in users]))


accepted_users = []
######
##  PDF UND USER VALIDATION
for user in users:
    # Decode the base64 encoded PDF
    # accepted_users.append(user)
    # continue

    print("Processing PDF for user", user["username"])
    try:
        data_url = user["attributes"][os.getenv("ATTR_UPLOAD_KEY")]
        base64pdf = data_url.replace('data:application/pdf;base64,', '')

        pdf_data = base64.b64decode(base64pdf)
        # Create an in-memory file-like object
        images = convert_from_bytes(pdf_data)

        image_to_save = images[0]

        image_to_save.save('{}/Signed_{}.pdf'.format(os.getenv("DOCUMENT_PATH"),str(user['username'])))

       # Now you can process each image with PIL
        for img in images:
            img.show()

        # Ask the user if the PDF is valid
        is_valid = input("Is the PDF valid? (y/n): ")
        if is_valid == "y":
            accepted_users.append(user)
        else:
            print("User", user["username"], "is not valid")
    except Exception as e:
        print("Error while processing PDF for user", user["username"], ":", e)
        print("User", user["username"], "is not valid")
        continue

######        

for user in accepted_users:
    userId = user["pk"]
    patch_active_url = url_base + f"core/users/{userId}/"
    
    user['is_active'] = True
    user['name']= user['attributes']['firstname']+ " " + user['attributes']['lastname']
    user["attributes"][os.getenv("ATTR_UPLOAD_KEY")] = 'saved'
    response = requests.patch(patch_active_url, headers=headers, json=user)    # Update the user's is_active field to True
    if response.status_code == 200:
        print("User", user["username"], "is now active")

        html_content = f"""
<html>
<head>
    <title>Confirmation of your registration</title>
</head>
<body>
    <h1>Confirmation of your registration in the PhaKIR platform</h1>
    <p>Dear {user["username"]},</p>
    <p>Your registration has been successfully processed.</p>
    <a href="https://auth.domain.de">Click here to access the PhaKIR platform</a>
    
    <p>Best regards,</p>
    <p>The PhaKIR-2024 Team</p>
</body>
</html>
"""
        print("Sending email to", user["email"])
        send_mail(user["email"], html_content)

    else:
        print("Failed to activate user", user["username"], "with status code:", response.status_code)
