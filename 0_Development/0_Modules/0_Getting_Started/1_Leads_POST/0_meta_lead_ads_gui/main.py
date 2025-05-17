import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
from auth import run_oauth_flow
from graph_api import get_pages, get_forms, get_recent_leads
from utils import load_config, reset_config
import json

class App(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Meta Lead Manager - Version 2")
        self.geometry("700x500")

        self.access_token = None
        self.page_token_map = {}
        self.current_stage = 0
        self.selected_page = None
        self.selected_form = None

        self.error_label = None

        self.build_initial_ui()

    def build_initial_ui(self):
        self.clear_window()
        self.connect_btn = tk.Button(self, text="Connect to Facebook", command=self.start_oauth, font=('Arial', 14))
        self.connect_btn.pack(expand=True)

    def start_oauth(self):
        self.connect_btn.config(state="disabled")
        error, token = run_oauth_flow()

        if token:
            self.access_token = token
            self.build_main_ui()
        else:
            self.connect_btn.config(state="normal")
            self.display_error(error or "Unknown error occurred during authentication.")

    def build_main_ui(self):
        self.clear_window()

        self.top_frame = tk.Frame(self)
        self.top_frame.pack(fill=tk.X)

        self.version_label = tk.Label(self.top_frame, text="Version 2", font=('Arial', 10))
        self.version_label.pack(side=tk.LEFT, padx=10)

        self.refresh_btn = tk.Button(self.top_frame, text="Refresh", command=self.refresh_current_stage)
        self.refresh_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.reset_btn = tk.Button(self.top_frame, text="Reset", command=self.reset_all)
        self.reset_btn.pack(side=tk.RIGHT, padx=5, pady=5)

        self.progress = tk.Frame(self)
        self.progress.pack(fill=tk.X)
        self.stage_labels = []
        self.stages = ["Select Page", "Select Form", "Test Configuration"]
        for i, name in enumerate(self.stages):
            label = tk.Label(self.progress, text=name, width=20, relief=tk.SUNKEN if i == 0 else tk.RAISED, bg="navy" if i == 0 else "gray", fg="white")
            label.pack(side=tk.LEFT, expand=True, fill=tk.X, padx=2)
            label.bind("<Button-1>", lambda e, i=i: self.switch_stage(i))
            self.stage_labels.append(label)

        self.content = tk.Frame(self)
        self.content.pack(fill=tk.BOTH, expand=True)
        self.stage_content = []

        for i in range(3):
            frame = tk.LabelFrame(self.content, text=f"Stage {i+1}: {self.stages[i]}")
            frame.pack(fill=tk.X, pady=10)
            self.stage_content.append(frame)

        # Stage 1 - Pages
        self.page_list = tk.Listbox(self.stage_content[0], height=5)
        self.page_list.pack(fill=tk.X, padx=10)
        self.page_list.bind("<<ListboxSelect>>", self.select_page)
        self.page_continue = tk.Button(self.stage_content[0], text="Continue", command=lambda: self.switch_stage(1))
        self.page_continue.pack()

        # Stage 2 - Forms
        self.form_list = tk.Listbox(self.stage_content[1], height=5)
        self.form_list.pack(fill=tk.X, padx=10)
        self.form_list.bind("<<ListboxSelect>>", self.select_form)
        self.form_continue = tk.Button(self.stage_content[1], text="Continue", command=lambda: self.switch_stage(2))
        self.form_continue.pack()

        self.form_back = tk.Button(self.stage_content[1], text="Back", command=lambda: self.switch_stage(0))
        self.form_back.pack()

        # Stage 3 - Leads
        self.test_btn = tk.Button(self.stage_content[2], text="Test", command=self.run_test)
        self.test_btn.pack(pady=5)

        self.leads_back = tk.Button(self.stage_content[2], text="Back", command=lambda: self.switch_stage(1))
        self.leads_back.pack()

        self.test_output = scrolledtext.ScrolledText(self.stage_content[2], height=10)
        self.test_output.pack(fill=tk.BOTH, expand=True, padx=10)

        self.error_label = tk.Label(self, text="", fg="red")
        self.error_label.pack(side=tk.BOTTOM, fill=tk.X)

        self.update_progress()
        self.switch_stage(0)

    def update_progress(self):
        for i, label in enumerate(self.stage_labels):
            if i == self.current_stage:
                label.config(bg="navy", relief=tk.SUNKEN)
            else:
                label.config(bg="gray", relief=tk.RAISED)

    def switch_stage(self, stage):
        self.current_stage = stage
        self.update_progress()
        for i, frame in enumerate(self.stage_content):
            frame.pack_forget()
        self.stage_content[stage].pack(fill=tk.X, pady=10)
        if stage == 0:
            self.load_pages()
        elif stage == 1:
            self.load_forms()

    def refresh_current_stage(self):
        if self.current_stage == 0:
            self.load_pages()
        elif self.current_stage == 1:
            self.load_forms()

    def load_pages(self):
        self.page_list.delete(0, tk.END)
        try:
            self.pages = get_pages(self.access_token)
            for page in self.pages:
                self.page_token_map[page["id"]] = page["access_token"]
                self.page_list.insert(tk.END, f"{page['name']} ({page['id']})")
        except Exception as e:
            self.display_error(f"Failed to load pages: {str(e)}")

    def select_page(self, e):
        index = self.page_list.curselection()
        if index:
            self.selected_page = self.pages[index[0]]

    def load_forms(self):
        self.form_list.delete(0, tk.END)
        try:
            if not self.selected_page:
                return
            page_id = self.selected_page['id']
            token = self.page_token_map.get(page_id)
            if not token:
                raise Exception("Page access token not found.")
            forms = get_forms(page_id, token)
            if not forms:
                self.display_error("No lead forms found for this page.")
            for form in forms:
                self.form_list.insert(tk.END, f"{form['name']} ({form['id']})")
            self.forms = forms
        except Exception as e:
            self.display_error(f"Failed to load forms: {str(e)}")

    def select_form(self, e):
        index = self.form_list.curselection()
        if index:
            self.selected_form = self.forms[index[0]]

    def run_test(self):
        self.test_output.delete(1.0, tk.END)
        if not self.selected_form:
            self.test_output.insert(tk.END, "No form selected.")
            return
        try:
            for lead in get_recent_leads(self.selected_form['id'], self.access_token):
                self.test_output.insert(tk.END, json.dumps(lead, indent=2) + "")
        except Exception as e:
            self.display_error(f"Failed to fetch leads: {str(e)}")

    def reset_all(self):
        if messagebox.askyesno("Confirm", "Reset and revoke token?"):
            reset_config()
            self.destroy()

    def clear_window(self):
        for widget in self.winfo_children():
            widget.destroy()

    def display_error(self, message):
        if self.error_label:
            self.error_label.config(text=message)

if __name__ == "__main__":
    App().mainloop()