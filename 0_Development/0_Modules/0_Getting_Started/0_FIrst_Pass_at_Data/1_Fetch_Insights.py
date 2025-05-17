import requests

ACCESS_TOKEN = 'EAAL0hsUCslgBOx7ZBgA3CMVm8zP6bQJ7A5AfXr7YJo99WmZB5MBSfpSjifNcgkI0YxGR9Oj6vpwifcDZBjRGs9jXzKd9KbkPw4lIV9kaPLAMTscee2riXRKbDo1ycFh8MfyZBjToamKJubMYqAwSUXZB4y3jy1ZBWZCbmZBFYGnF8alZBdFr5CIsC36Xns3nNkTm1Gntg1Do1Nxr9aKx88eS80SPRPcOgYQuaeZCMI'
CAMPAIGN_ID = '120210803897960111'  # just the numeric ID, no "act_"
API_VERSION = 'v22.0'

url = f'https://graph.facebook.com/{API_VERSION}/{CAMPAIGN_ID}/insights'

params = {
    'access_token': ACCESS_TOKEN,
    'fields': (
        'spend,impressions,reach,'
        'actions,cost_per_action_type'
    ),
    'date_preset': 'last_30d',  # Or use time_range for custom
    'level': 'campaign'
}

response = requests.get(url, params=params)

if response.ok:
    data = response.json().get('data', [])
    for entry in data:
        print(f"Spend: ${entry.get('spend')}")
        print(f"Reach: {entry.get('reach')}")
        print(f"Impressions: {entry.get('impressions')}")
        
        # Extract On-Facebook Leads
        actions = entry.get('actions', [])
        for action in actions:
            if action['action_type'] == 'lead':
                print(f"On-Facebook Leads: {action['value']}")

        # Extract Cost per Lead
        cpl = entry.get('cost_per_action_type', [])
        for item in cpl:
            if item['action_type'] == 'lead':
                print(f"Cost per Lead: ${item['value']}")
else:
    print("Error:", response.json())
