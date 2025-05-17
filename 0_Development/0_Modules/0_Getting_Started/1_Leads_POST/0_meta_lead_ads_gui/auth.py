import webbrowser
import http.server
import ssl
import threading
import requests
import json
import urllib.parse
import time

from utils import save_config

APP_ID = '831809621504600'
APP_SECRET = '875adfa3f56fe47586f232f14cd411c5'
REDIRECT_URI = 'https://localhost:5000/'
SCOPES = ['pages_show_list', 'ads_management', 'business_management', 'leads_retrieval', 'pages_read_engagement', 'pages_manage_ads']
AUTH_URL = f"https://www.facebook.com/v22.0/dialog/oauth?client_id={APP_ID}&redirect_uri={urllib.parse.quote(REDIRECT_URI)}&scope={','.join(SCOPES)}&response_type=code"

TOKEN_URL = "https://graph.facebook.com/v22.0/oauth/access_token"
LONG_TOKEN_URL = "https://graph.facebook.com/v22.0/oauth/access_token"

class OAuthHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        parsed = urllib.parse.urlparse(self.path)
        query = urllib.parse.parse_qs(parsed.query)
        self.server.auth_code = query.get('code', [None])[0]
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Authorization successful! You may now close this window.")

def start_https_server():
    try:
        server_address = ('localhost', 5000)
        httpd = http.server.HTTPServer(server_address, OAuthHandler)
        print("✅ HTTP server started")

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_SERVER)
        context.load_cert_chain(certfile='cert.pem', keyfile='key.pem')
        httpd.socket = context.wrap_socket(httpd.socket, server_side=True)

        print("✅ SSL context applied successfully")

        thread = threading.Thread(target=httpd.handle_request)
        thread.start()
        return httpd

    except Exception as e:
        print("❌ HTTPS server failed to start:", str(e))
        return None

def exchange_code_for_token(code):
    params = {
        'client_id': APP_ID,
        'redirect_uri': REDIRECT_URI,
        'client_secret': APP_SECRET,
        'code': code
    }
    res = requests.get(TOKEN_URL, params=params)
    if res.status_code != 200:
        raise Exception(res.json().get("error", {}).get("message", "Unknown error"))
    return res.json()['access_token']

def exchange_for_long_lived_token(short_token):
    params = {
        'grant_type': 'fb_exchange_token',
        'client_id': APP_ID,
        'client_secret': APP_SECRET,
        'fb_exchange_token': short_token
    }
    res = requests.get(LONG_TOKEN_URL, params=params)
    if res.status_code != 200:
        raise Exception(res.json().get("error", {}).get("message", "Unknown error"))
    return res.json()['access_token']

def run_oauth_flow():
    webbrowser.open(AUTH_URL)
    server = start_https_server()

    for _ in range(3):
        server.handle_request()
        code = getattr(server, 'auth_code', None)
        if not code:
            time.sleep(1)
            continue
        try:
            short_token = exchange_code_for_token(code)
            long_token = exchange_for_long_lived_token(short_token)
            save_config({'access_token': long_token})
            return None, long_token
        except Exception as e:
            return str(e), None
    return "OAuth flow failed after 3 attempts.", None