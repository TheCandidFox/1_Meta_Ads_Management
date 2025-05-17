import requests
import json

GRAPH_API_URL = "https://graph.facebook.com/v22.0"

def get_pages(access_token):
    url = f"{GRAPH_API_URL}/me/accounts?fields=name,id,access_token"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json().get("data", [])

def get_forms(page_id, page_access_token):
    url = f"{GRAPH_API_URL}/{page_id}/leadgen_forms?fields=id,name"
    headers = {"Authorization": f"Bearer {page_access_token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json().get("data", [])

def get_recent_leads(form_id, access_token):
    url = f"{GRAPH_API_URL}/{form_id}/leads?limit=3"
    headers = {"Authorization": f"Bearer {access_token}"}
    res = requests.get(url, headers=headers)
    res.raise_for_status()
    return res.json().get("data", [])