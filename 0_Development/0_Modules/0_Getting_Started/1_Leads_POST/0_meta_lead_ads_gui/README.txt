== Meta Lead Ads Local GUI ==

1. Replace `your_app_id` and `your_app_secret` in `auth.py` with your Meta app credentials.
2. Generate a self-signed certificate using OpenSSL:

   openssl req -new -x509 -keyout key.pem -out cert.pem -days 365 -nodes

3. Run `main.py` to start the Tkinter GUI.
4. On first launch, you'll go through OAuth and a long-lived token will be saved.
5. Use Reset to revoke the token and clear local data.

Make sure you have:
- Python 3.9+
- `requests` installed

Optional: install `pyopenssl` if needed for HTTPS server compatibility.