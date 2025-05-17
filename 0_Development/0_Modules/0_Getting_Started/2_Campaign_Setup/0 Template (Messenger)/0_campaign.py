from facebook_business.api import FacebookAdsApi
from facebook_business.adobjects.adaccount import AdAccount
from facebook_business.adobjects.campaign import Campaign


# --- CONFIGURE ACCESS ---
ACCESS_TOKEN = 'EAAL0hsUCslgBOzNBZARXh3kreFHJS13AKPCcoyPzfMvm9fmA0uoFZADXdniHKGm1RI72zrLdZAfPZCgBXPmhZAykbtBrpJuUw63fQZCp2hSa2lXvubEsHWQJLKg4ylAeObL4t9qMdZBsape58tqc8pY8qtXgBTXcCYRfKc20VYcPNdnk0f4li7YYqfcqNCnEx6w9CxbMc7zZCiysZA5ysFziLtVqpriqZCnIBkASEZD'
AD_ACCOUNT_ID = 'act_786767373171681'
APP_ID = '831809621504600'
APP_SECRET = '875adfa3f56fe47586f232f14cd411c5'


FacebookAdsApi.init(APP_ID, APP_SECRET, ACCESS_TOKEN)


# --- CAMPAIGN TEMPLATE FUNCTION ---
def create_base_leads_campaign(name, daily_budget_usd, special_ad_categories=None):
    if special_ad_categories is None:
        special_ad_categories = []

    account = AdAccount(AD_ACCOUNT_ID)

    params = {
        'name': name,
        'objective': 'OUTCOME_LEADS',  # ✅ We picked "Leads"
        'buying_type': 'AUCTION',  # ✅ Matches performance intent
        'status': Campaign.Status.paused,  # Pause by default so it's safe to modify later
        'campaign_budget_optimization': True,  # Campaign-level budget (Advantage+ style)
        'daily_budget': str(int(daily_budget_usd * 100)),  # Convert to cents
        'special_ad_categories': special_ad_categories,  # Empty list or e.g., ['HOUSING']
        "bid_strategy": "LOWEST_COST_WITHOUT_CAP"  # <- This is the smart switch
    }

    campaign = account.create_campaign(params=params)
    return campaign

# --- USE CASE EXAMPLE ---
campaign = create_base_leads_campaign(
    name="Attempt at new Template",
    daily_budget_usd=9.50,
    special_ad_categories=[]  # Can also be ['HOUSING'], etc.
)


print(f"✅ Campaign Created: {campaign['id']}")

