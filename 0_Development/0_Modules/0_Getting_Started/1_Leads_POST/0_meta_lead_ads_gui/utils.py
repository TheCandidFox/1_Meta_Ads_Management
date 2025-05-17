import json
import os
import requests

CONFIG_FILE = "config.json"

def save_config(data):
    with open(CONFIG_FILE, 'w') as f:
        json.dump(data, f, indent=2)

def load_config():
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, 'r') as f:
            return json.load(f)
    return {}

def reset_config():
    config = load_config()
    if 'access_token' in config:
        revoke_token(config['access_token'])
    if os.path.exists(CONFIG_FILE):
        os.remove(CONFIG_FILE)

def revoke_token(token):
    try:
        uid = requests.get("https://graph.facebook.com/me", params={'access_token': token}).json()['id']
        requests.delete(f"https://graph.facebook.com/{uid}/permissions", params={'access_token': token})
    except:
        pass