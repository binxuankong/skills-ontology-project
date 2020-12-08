import requests
import json

# Request for access token from Emsi
# Given the client_id and secret
def get_access_token(client_id, secret, scope='emsi_open'):
    url = "https://auth.emsicloud.com/connect/token"
    payload = "client_id={}&client_secret={}&grant_type=client_credentials&scope={}".format(client_id, secret, scope)
    headers = {'content-type': 'application/x-www-form-urlencoded'}
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json().get("access_token")


# Check health of Emsi service
def check_health(access_token):
    url = "https://emsiservices.com/skills/status"
    headers = {'authorization': 'Bearer {}'.format(access_token)}
    response = requests.request("GET", url, headers=headers)
    return response.json()['data']


# Extract skills from Emsi based on query
def get_emsi_skills(query, access_token, limit=10, soft_skills=False, certification=False):
    """
    query: skills to search for
    access_token: token for authorization
    limit: maximum number of skills to return
    ST1: Hard skills - unique (or technical) skills related to a specialty
    ST2: Soft skills - common (or human) skills which are broad statements of ability
    ST3: Certification - recognizable qualification standards assigned by industry or education bodies
    """
    url = "https://emsiservices.com/skills/versions/latest/skills"
    type_ids = "ST1"
    if soft_skills:
        type_ids += ",ST2"
    if certification:
        type_ids += ",ST3"
    querystring = {"q": query, "typeIds": type_ids, "fields": "id,name,type,infoUrl", "limit": str(limit)}
    headers = {'authorization': 'Bearer {}'.format(access_token)}
    response = requests.request("GET", url, headers=headers, params=querystring)
    return response.json()['data']


# Extract skills from text
def extract_skills(text, access_token, confidence_threshold=0.6):
    url = "https://emsiservices.com/skills/versions/latest/extract"
    payload = {"text": text, "confidenceThreshold": confidence_threshold}
    headers = {'authorization': 'Bearer {}'.format(access_token), 'content-type': 'text/plain'}
    response = requests.request("POST", url, data=payload, headers=headers)
    return response.json()['data']