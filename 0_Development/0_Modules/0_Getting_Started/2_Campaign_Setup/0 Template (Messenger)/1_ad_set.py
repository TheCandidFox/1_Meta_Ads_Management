from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign


# --- CONFIGURE ACCESS ---
ACCESS_TOKEN = 'EAAL0hsUCslgBO3CC6PSONU2t7AFZBAWQxiZA7ZBpBhOSr8ZBycwMx4ElfHyZCxCod8ZCGBfSkSmdZCEwWz8eVoHKD4s2zJzqPQe531HtxdJWgcAS9afw7ZCMWTgPH8punBenZC7PzHqG7aQmS2XQ0KU4VAJYKZAfS5HDva9xk97kTlGVrs4ZADLy5RpBTelGf8cucAP3p7Ely2JjWStKgw0hkSuIxVZBriaCHO9mZBWpe'
AD_ACCOUNT_ID = 'act_786767373171681'
APP_ID = '831809621504600'
APP_SECRET = '875adfa3f56fe47586f232f14cd411c5'


FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)


# Use the campaign ID returned when you created the campaign
CAMPAIGN_ID = '120222181727540111'

campaign = Campaign(CAMPAIGN_ID).api_get(fields=[
    Campaign.Field.id,
    Campaign.Field.name,
    Campaign.Field.status,
    Campaign.Field.objective,
])

print("Campaign ID:", campaign[Campaign.Field.id])
print("Name:", campaign[Campaign.Field.name])
print("Status:", campaign[Campaign.Field.status])
print("Objective:", campaign[Campaign.Field.objective])
