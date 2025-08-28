import json
import os
import requests
from requests.auth import HTTPBasicAuth
from dotenv import load_dotenv

CRED = '\033[91m'
CEND = '\033[0m'
CBLUE = '\033[94m'

# load .env 
load_dotenv()

# Arguments
parser = argparse.ArgumentParser()
parser.add_argument("--root", default=os.getenv("PH_ROOT", "./phakir"),
                    help="Root directory for evaluation setup")
parser.add_argument("--timeout", type=int, default=int(os.getenv("PH_PULL_TIMEOUT", "300")),
                    help="Timeout in seconds for docker pull")
args = parser.parse_args()

CRED = '\033[91m'
CEND = '\033[0m'
CBLUE = '\033[94m'

# Registry config
registry_url = os.getenv("PH_URL")
registry = os.getenv("PH_REGISTRY")
user = os.getenv("PH_USER")
password = os.getenv("PH_PASS")

url = f'{registry_url}/v2/_catalog'

# GET-Anfrage mit Basic Auth
image_response = requests.get(url, auth=HTTPBasicAuth(user, password))

# Überprüfen des Statuscodes der Antwort
if image_response.status_code == 200:
    # Erfolgreiche Anfrage, Ausgabe der Antwort
    repositories = image_response.json()["repositories"]
    print(CBLUE +f"{len(repositories)} submssions catched.")#image_response.json())
else:
    # Fehler bei der Anfrage, Ausgabe des Statuscodes
    print(CRED +f'Error: {image_response.status_code}')  

submission = {'keypoint_estimation':[],'instrument_segmentation':[],'phase_recognition':[] }


for repo in repositories:
    
    tag_url = f'{registry_url}/v2/{repo}/tags/list'
    
    docker_user = repo.split("/")[0]
    docker_submission_user = repo.split("/")[1]
    tags = []
    
        # GET-Anfrage mit Basic Auth
    tag_response = requests.get(tag_url, auth=HTTPBasicAuth(user, password))

    # Überprüfen des Statuscodes der Antwort
    if tag_response.status_code == 200:
        # Erfolgreiche Anfrage, Ausgabe der Antwort
        tags=tag_response.json()["tags"]
    else:
        # Fehler bei der Anfrage, Ausgabe des Statuscodes
        print(CRED +f'Error: {tag_response.status_code}')
    
    for t in tags:
        c = False
        if("keypoint" in t):
            submission["keypoint_estimation"].append({"phakir_user": docker_user, "phakir_submission_team": docker_submission_user,"tag": t, "all_tags": tags})
            c=True
        if("segmentation" in t):
            submission["instrument_segmentation"].append({"phakir_user": docker_user, "phakir_submission_team": docker_submission_user,"tag": t, "all_tags": tags})
            c=True
        if("phase" in t):
            submission["phase_recognition"].append({"phakir_user": docker_user, "phakir_submission_team": docker_submission_user,"tag": t, "all_tags": tags})
            c=True
            
        if(not c):
            print(CRED + f'Error - unknown tag: {t}' + CEND)
    

import subprocess, time

login_command = f'docker login -u {user} -p {password} {registry}'
result = subprocess.run(login_command, shell=True, text=True, capture_output=True)
if result.returncode != 0:
    print(CRED + f'ERROR - login: {result.stderr}' + CEND)
else:
    print(CBLUE+'login sucessful.'+CEND)
    

# Ein Docker-Image ziehen
for sub, s_list in submission.items():
    for s in s_list:
        image_name = f'{s["phakir_user"]}/{s["phakir_submission_team"]}:{sub}'
        full_image_name = f'{registry}{image_name}'
        print(CBLUE + 'Pull docker image' + CEND)
        
        pull_command = f'docker pull {full_image_name}'
        process = subprocess.Popen(pull_command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
        
        # Live-Ausgabe der Befehlsausführung
        while True:
            output = process.stdout.readline()
            if process.poll() is not None and output == b'':
                break
            if output:
                print(output.decode(), end='')
        
        try:
            process.wait(timeout=300)  # 5 minutes timeout
        except subprocess.TimeoutExpired:
            print(CRED + f'Timeout - docker pulling {full_image_name} took too long.' + CEND)
        
        if process.returncode != 0:
            print(CRED + f'Error - docker pulling {full_image_name}' + CEND)
        else:
            print(CBLUE + 'Docker image pulled successfully.' + CEND)
                
     
# Create Directories
root_path = "/home/leo/phakir"

mnt_path = f"{root_path}/input"
os.makedirs(mnt_path, exist_ok=True)

for key in submission.keys():    
    path = f"{root_path}/{key}"
    os.makedirs(path, exist_ok=True)

    for sub in submission[key]:
        path = f"{root_path}/{key}/{sub['phakir_submission_team']}"
        os.makedirs(path, exist_ok=True)

        txt_path = f"{path}/info.txt"
        with open(txt_path, 'w') as file:
            # Writing the dictionary in a pretty format
            file.write(json.dumps(sub, indent=4))
            
        # Create docker-compose file from repository:tag 
        # Copy therefore the template from /home/leo/phakir/docker-compose.yml.template and replace <phakir> with the repository:tag
        try:
            with open(f"{root_path}/docker-compose.yml.template", 'r') as file:
                filedata = file.read()
                filedata = filedata.replace('<phakir>', f'{registry}{sub["phakir_user"]}/{sub["phakir_submission_team"]}:{key}')
            with open(f"{path}/docker-compose.yml", 'w') as file:
                file.write(filedata)
        except:
            print(CRED + f'Error - docker-compose template' + CEND)   
        print(CBLUE+f"docker compose file created"+CEND)   
            
        path = f"{root_path}/{key}/{sub['phakir_submission_team']}/outputs"
        os.makedirs(path, exist_ok=True)
        path = f"{root_path}/{key}/{sub['phakir_submission_team']}/inputs"
        #os.makedirs(path, exist_ok=True)
        # mount mnt_path into input
        # Erstellen Sie den symbolischen Link, wenn er noch nicht existiert
        if not os.path.exists(path):
            os.symlink(mnt_path, path)
            print(CBLUE+f"Symbolic Link created: {path} -> {mnt_path}"+CEND)
        else:
            print(f"Path already exists: {path}")
        
