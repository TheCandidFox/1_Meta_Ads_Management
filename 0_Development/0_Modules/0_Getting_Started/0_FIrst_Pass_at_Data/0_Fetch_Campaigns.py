# Token Endpoint: https://developers.facebook.com/tools/explorer/

import requests

ACCESS_TOKEN = 'EAAL0hsUCslgBOx7ZBgA3CMVm8zP6bQJ7A5AfXr7YJo99WmZB5MBSfpSjifNcgkI0YxGR9Oj6vpwifcDZBjRGs9jXzKd9KbkPw4lIV9kaPLAMTscee2riXRKbDo1ycFh8MfyZBjToamKJubMYqAwSUXZB4y3jy1ZBWZCbmZBFYGnF8alZBdFr5CIsC36Xns3nNkTm1Gntg1Do1Nxr9aKx88eS80SPRPcOgYQuaeZCMI'
AD_ACCOUNT_ID = 'act_786767373171681'  # Include 'act_' prefix
API_VERSION = 'v22.0'

url = f"https://graph.facebook.com/{API_VERSION}/{AD_ACCOUNT_ID}/campaigns"

params = {
    'access_token': ACCESS_TOKEN,
    'fields': 'id,name,status',
    'limit': 50  # You can increase this if needed
}

response = requests.get(url, params=params)

if response.ok:
    campaigns = response.json().get('data', [])
    print("Campaigns:")
    for campaign in campaigns:
        print(f"- {campaign['name']} (ID: {campaign['id']}, Status: {campaign['status']})")
else:
    print("Error fetching campaigns:")
    print(response.json())
