import tkinter as tk
from tkinter import ttk, messagebox
import requests
import time

# ==== CONFIG ====
ACCESS_TOKEN = 'EAAL0hsUCslgBO91kImIMGeGrspCVRAtp877j4CDfzMAzDBERVabwXiqdjWD0OOQQPb2zabWXs4zhDvlouBSTIWqwH25y3py6Y73VndThAopSeeAJ7RHpIMWsbzBafr9df4G0fqzNOIZBDRgzDzSoacVCuO1OuVZBSHc3mPZCxt2veiWFWrcCAOL7EbF5G1gDZB4Fh3kSjGioOmoDTX0VTsjgUiBQPAti8rwZD'
AD_ACCOUNT_ID = 'act_786767373171681'
API_VERSION = 'v22.0'
# ================

# ====================
# Meta API Functions
# ====================
def fetch_campaigns():
    url = f"https://graph.facebook.com/{API_VERSION}/{AD_ACCOUNT_ID}/campaigns"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'id,name,status',
        'limit': 100
    }
    response = requests.get(url, params=params)
    if response.ok:
        campaigns = response.json().get('data', [])
        # Sort ACTIVE first
        return sorted(campaigns, key=lambda c: 0 if c['status'] == 'ACTIVE' else 1)
    else:
        messagebox.showerror("Error", f"Failed to fetch campaigns:\n{response.json()}")
        return []

def get_campaign_status(campaign_id):
    url = f"https://graph.facebook.com/{API_VERSION}/{campaign_id}"
    params = {
        'access_token': ACCESS_TOKEN,
        'fields': 'status'
    }
    response = requests.get(url, params=params)
    if response.ok:
        return response.json().get('status')
    return None

def update_campaign_status(campaign_id, new_status):
    url = f"https://graph.facebook.com/{API_VERSION}/{campaign_id}"
    params = {
        'access_token': ACCESS_TOKEN,
        'status': new_status
    }
    response = requests.post(url, data=params)
    return response.ok

# ====================
# GUI Setup
# ====================
class CampaignControllerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Meta Campaign Controller")
        self.selected_campaign = None
        self.campaigns = fetch_campaigns()

        self.create_campaign_list()
        self.create_status_frame()

    def create_campaign_list(self):
        frame = tk.Frame(self.root)
        frame.pack(side=tk.LEFT, fill=tk.Y)

        label = tk.Label(frame, text="Select a Campaign:")
        label.pack(pady=5)

        # Scrollable campaign list
        canvas = tk.Canvas(frame, width=350, height=200)
        scrollbar = ttk.Scrollbar(frame, orient="vertical", command=canvas.yview)
        self.campaign_list_frame = tk.Frame(canvas)

        self.campaign_list_frame.bind(
            "<Configure>",
            lambda e: canvas.configure(scrollregion=canvas.bbox("all"))
        )

        canvas.create_window((0, 0), window=self.campaign_list_frame, anchor="nw")
        canvas.configure(yscrollcommand=scrollbar.set)

        canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

        for campaign in self.campaigns:
            button_text = f"{campaign['name']} ({campaign['id']}) [{campaign['status']}]"
            b = tk.Button(self.campaign_list_frame, text=button_text, width=40, anchor='w',
                          command=lambda c=campaign: self.load_campaign_controls(c))
            b.pack(pady=2, padx=5)

    def create_status_frame(self):
        self.status_frame = tk.Frame(self.root)
        self.status_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True)

    def load_campaign_controls(self, campaign):
        self.selected_campaign = campaign
        for widget in self.status_frame.winfo_children():
            widget.destroy()

        status = get_campaign_status(campaign['id'])

        label = tk.Label(self.status_frame, text=f"Selected Campaign:\n{campaign['name']}\nStatus: {status}", font=('Arial', 12))
        label.pack(pady=10)

        button_on = tk.Button(self.status_frame, text="Turn On", width=20,
                              command=lambda: self.toggle_campaign('ACTIVE'))
        button_pause = tk.Button(self.status_frame, text="Pause", width=20,
                                 command=lambda: self.toggle_campaign('PAUSED'))
        button_on.pack(pady=5)
        button_pause.pack(pady=5)

        self.progress_label = tk.Label(self.status_frame, text="", font=('Arial', 10))
        self.progress_label.pack(pady=10)

    def toggle_campaign(self, desired_status):
        campaign_id = self.selected_campaign['id']
        current_status = get_campaign_status(campaign_id)

        if current_status == desired_status:
            msg = f"Campaign is already {desired_status}."
            self.progress_label.config(text=msg)
            return

        self.progress_label.config(text="Step 1: Sending request...")
        self.root.update()
        success = update_campaign_status(campaign_id, desired_status)
        time.sleep(1)

        if not success:
            self.progress_label.config(text="❌ Failed to send request.")
            return

        self.progress_label.config(text="Step 2: Validating...")
        self.root.update()
        time.sleep(3)

        confirmed_status = get_campaign_status(campaign_id)
        if confirmed_status == desired_status:
            self.progress_label.config(text="Step 3: ✅ Success! Campaign updated.")
            self.refresh_campaign_list()
        else:
            self.progress_label.config(text="❌ Validation failed. Status unchanged.")

    def refresh_campaign_list(self):
        # Refresh all buttons after a change
        for widget in self.campaign_list_frame.winfo_children():
            widget.destroy()
        self.campaigns = fetch_campaigns()
        for campaign in self.campaigns:
            button_text = f"{campaign['name']} ({campaign['id']}) [{campaign['status']}]"
            b = tk.Button(self.campaign_list_frame, text=button_text, width=40, anchor='w',
                          command=lambda c=campaign: self.load_campaign_controls(c))
            b.pack(pady=2, padx=5)

# ====================
# Run App
# ====================
if __name__ == "__main__":
    root = tk.Tk()
    app = CampaignControllerApp(root)
    root.mainloop()
