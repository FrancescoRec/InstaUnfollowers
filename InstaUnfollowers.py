import os
import sys
import json
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
import threading
from datetime import datetime
import webbrowser

from PIL import Image, ImageTk  # Pillow for icon/image

# Helper function to handle resource paths when bundled as an executable
def resource_path(relative_path):
    """Get absolute path to resource, works for dev and for PyInstaller"""
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    
    return os.path.join(base_path, relative_path)

class InstagramJSONAnalyzer:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram JSON Analyzer 🔍")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)

        # ---- Set window icon ----
        try:
            icon_path = resource_path("instaunfollowers_icon.png")
            self.root.iconphoto(False, tk.PhotoImage(file=icon_path))
            
            # Set taskbar icon on Windows
            if os.name == 'nt':
                try:
                    from ctypes import windll
                    ico_path = resource_path("instaunfollowers_icon.ico")
                    if os.path.exists(ico_path):
                        windll.shell32.SetCurrentProcessExplicitAppUserModelID("InstaUnfollowers")
                        self.root.iconbitmap(default=ico_path)
                except Exception as e:
                    print("Could not set taskbar icon:", e)
        except Exception as e:
            print("Icon not loaded:", e)

        # ---- Variables ----
        self.following_file = tk.StringVar()
        self.followers_file = tk.StringVar()

        self.following_count = tk.IntVar(value=0)
        self.followers_count = tk.IntVar(value=0)
        self.mutual_count = tk.IntVar(value=0)
        self.not_following_back_count = tk.IntVar(value=0)
        self.you_dont_follow_count = tk.IntVar(value=0)

        self.following_data = []
        self.followers_data = []
        self.not_following_back = []
        self.you_dont_follow = []
        self.mutual = []

        # ---- Instagram Color Theme ----
        self.bg_color = "#fdfdfd"
        self.accent_color = "#E1306C"      # Pink
        self.secondary_color = "#833AB4"   # Purple
        self.text_color = "#262626"
        self.chart_colors = {
            "mutual": "#833AB4",            # Purple
            "not_following_back": "#FD1D1D", # Red
            "you_dont_follow": "#FCAF45"    # Orange
        }

        self.root.configure(bg=self.bg_color)

        # ---- Styles ----
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Header.TLabel",
                             font=("Helvetica", 16, "bold"),
                             background=self.bg_color,
                             foreground=self.accent_color)
        self.style.configure("Stats.TLabel",
                             font=("Helvetica", 14),
                             background=self.bg_color,
                             foreground=self.text_color)
        self.style.configure("Accent.TButton",
                             font=("Helvetica", 12, "bold"))

        # ---- Build UI ----
        self.create_widgets()

    def show_how_to_use(self):
        """Show README content in a popup window."""
        readme_file = resource_path("readME.md")  # Use resource_path to find README
        if not os.path.exists(readme_file):
            messagebox.showerror("Error", "README file not found in the app folder.")
            return

        try:
            with open(readme_file, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception as e:
            messagebox.showerror("Error", f"Failed to open README: {e}")
            return

        # Create a new top-level window
        help_window = tk.Toplevel(self.root)
        help_window.title("How to Use - Instructions")
        help_window.geometry("700x500")

        text_area = tk.Text(help_window, wrap=tk.WORD)
        text_area.pack(fill=tk.BOTH, expand=True)

        text_area.insert(tk.END, content)
        text_area.config(state=tk.DISABLED)

        close_btn = ttk.Button(help_window, text="Close", command=help_window.destroy)
        close_btn.pack(pady=5)

    def create_widgets(self):
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)

        # ---- Header Image ----
        try:
            img_path = resource_path("instaunfollowers_icon.png")
            img = Image.open(img_path).resize((64, 64))
            self.header_image = ImageTk.PhotoImage(img)
            img_label = tk.Label(main_frame, image=self.header_image, bg=self.bg_color)
            img_label.pack()
        except Exception as e:
            print("Header image failed to load:", e)

        # ---- Title ----
        title_label = ttk.Label(main_frame, text="Instagram JSON Analyzer 🔍",
                                font=("Helvetica", 20, "bold"),
                                foreground=self.accent_color,
                                background=self.bg_color)
        title_label.pack(pady=(10, 10))

        # ---- How to Use Button ----
        howto_btn = ttk.Button(main_frame, text="How to Use 📖", command=self.show_how_to_use)
        howto_btn.pack(pady=(0, 10))

        # ---- File Select Frame ----
        file_frame = ttk.LabelFrame(main_frame, text="Select JSON Files", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Label(file_frame, text="Following JSON File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.following_file, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse...", command=lambda: self._browse_file(self.following_file)).grid(row=0, column=2, padx=5, pady=5)

        ttk.Label(file_frame, text="Followers JSON File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.followers_file, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse...", command=lambda: self._browse_file(self.followers_file)).grid(row=1, column=2, padx=5, pady=5)

        # ---- Action Buttons ----
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))

        ttk.Button(action_frame, text="Analyze Data", command=self.analyze_data).pack(side=tk.LEFT, padx=5)
        ttk.Button(action_frame, text="Save Report", command=self.save_report).pack(side=tk.LEFT, padx=5)

        # ---- Notebook Tabs ----
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)

        self._create_summary_tab()
        self._create_treeview_tabs()

        # ---- Footer ----
        self.status_label = ttk.Label(main_frame, text="Ready. Select JSON files to begin.", background=self.bg_color)
        self.status_label.pack(pady=5)

    def _create_summary_tab(self):
        summary = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(summary, text="Summary")

        stats = ttk.LabelFrame(summary, text="Statistics", padding=10)
        stats.pack(fill=tk.X)

        stats_items = [
            ("Following:", self.following_count),
            ("Followers:", self.followers_count),
            ("Mutual Connections:", self.mutual_count),
            ("Not Following You Back:", self.not_following_back_count),
            ("You Don't Follow Back:", self.you_dont_follow_count)
        ]

        for i, (label, var) in enumerate(stats_items):
            ttk.Label(stats, text=label).grid(row=i, column=0, sticky=tk.W)
            ttk.Label(stats, textvariable=var, font=("Helvetica", 12, "bold")).grid(row=i, column=1, sticky=tk.W)

        self.canvas = tk.Canvas(summary, bg="white", height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True)

    def _create_treeview_tabs(self):
        # Tabs for results
        self.tree_tabs = {
            "Not Following You Back 💔": [],
            "You Don't Follow Back 🤔": [],
            "Mutual Connections 👍": []
        }

        self.treeviews = {}

        for name in self.tree_tabs.keys():
            frame = ttk.Frame(self.notebook, padding=10)
            self.notebook.add(frame, text=name)
            tree = self._create_treeview(frame)
            self.treeviews[name] = tree

    def _create_treeview(self, parent):
        columns = ("username", "profile_url", "timestamp")
        tree = ttk.Treeview(parent, columns=columns, show="headings")

        for col in columns:
            tree.heading(col, text=col.capitalize())
            tree.column(col, width=180)

        vsb = ttk.Scrollbar(parent, orient="vertical", command=tree.yview)
        tree.configure(yscrollcommand=vsb.set)

        tree.grid(row=0, column=0, sticky="nsew")
        vsb.grid(row=0, column=1, sticky="ns")

        parent.rowconfigure(0, weight=1)
        parent.columnconfigure(0, weight=1)

        tree.bind("<Double-1>", self._open_profile)

        return tree

    def _browse_file(self, var):
        filename = filedialog.askopenfilename(filetypes=[("JSON files", "*.json")])
        if filename:
            var.set(filename)

    def _open_profile(self, event):
        tree = event.widget
        selected = tree.selection()
        if selected:
            url = tree.item(selected[0])["values"][1]
            if url:
                webbrowser.open(url)

    def _update_status(self, text):
        self.status_label.config(text=text)
        self.root.update_idletasks()

    def analyze_data(self):
        if not os.path.exists(self.following_file.get()) or not os.path.exists(self.followers_file.get()):
            messagebox.showerror("Error", "Please select both valid JSON files.")
            return

        self._update_status("Analyzing...")
        threading.Thread(target=self._run_analysis).start()

    def _run_analysis(self):
        # Parse JSON files
        self.following_data = self._parse_json(self.following_file.get())
        self.followers_data = self._parse_json(self.followers_file.get())

        # Extract just the usernames as sets for comparison (like in find_not_following_back.py)
        following_usernames = {u['username'] for u in self.following_data}
        followers_usernames = {u['username'] for u in self.followers_data}
        
        # Find intersection and differences, exactly like in find_not_following_back.py
        mutual_usernames = following_usernames.intersection(followers_usernames)
        not_following_back_usernames = following_usernames - followers_usernames
        you_dont_follow_usernames = followers_usernames - following_usernames
        
        # Filter the original data structures to preserve all info like timestamps
        self.mutual = [u for u in self.following_data if u['username'] in mutual_usernames]
        self.not_following_back = [u for u in self.following_data if u['username'] in not_following_back_usernames]
        self.you_dont_follow = [u for u in self.followers_data if u['username'] in you_dont_follow_usernames]

        self.root.after(0, self._update_results)

    def _parse_json(self, filepath):
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                data = json.load(f)
            result = []
            items = data.get("relationships_following") if "relationships_following" in data else data
            for item in items:
                if "string_list_data" in item:
                    u = item["string_list_data"][0]
                    result.append({
                        "username": u.get("value"),
                        "profile_url": u.get("href"),
                        "timestamp": u.get("timestamp", 0)
                    })
            return result
        except Exception as e:
            messagebox.showerror("Error", f"Failed to parse {filepath}: {e}")
            return []

    def _update_results(self):
        # Update counts
        self.following_count.set(len(self.following_data))
        self.followers_count.set(len(self.followers_data))
        self.mutual_count.set(len(self.mutual))
        self.not_following_back_count.set(len(self.not_following_back))
        self.you_dont_follow_count.set(len(self.you_dont_follow))

        # Update treeviews
        self._populate_treeview("Not Following You Back 💔", self.not_following_back)
        self._populate_treeview("You Don't Follow Back 🤔", self.you_dont_follow)
        self._populate_treeview("Mutual Connections 👍", self.mutual)

        self._update_status("Analysis complete.")

    def _populate_treeview(self, tab, data):
        tree = self.treeviews[tab]
        tree.delete(*tree.get_children())

        def fmt_date(ts):
            return datetime.fromtimestamp(ts).strftime('%Y-%m-%d') if ts else ""

        for u in data:
            tree.insert("", "end", values=(u['username'], u['profile_url'], fmt_date(u['timestamp'])))

    def save_report(self):
        if not self.following_data:
            messagebox.showwarning("No data", "Please analyze first.")
            return

        filepath = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt")])
        if not filepath:
            return

        try:
            with open(filepath, "w", encoding="utf-8") as f:
                # Write header and summary - similar to find_not_following_back.py
                f.write(f"Instagram Report - {datetime.now()}\n\n")
                f.write(f"Total accounts you're following: {self.following_count.get()}\n")
                f.write(f"Total accounts following you: {self.followers_count.get()}\n")
                f.write(f"Mutual connections: {self.mutual_count.get()}\n")
                f.write(f"Not following you back: {self.not_following_back_count.get()}\n")
                f.write(f"You don't follow them: {self.you_dont_follow_count.get()}\n\n")
                
                # Write accounts not following back - similar output style to find_not_following_back.py
                f.write("=== ACCOUNTS THAT DON'T FOLLOW YOU BACK ===\n")
                if self.not_following_back:
                    for i, item in enumerate(sorted(self.not_following_back, key=lambda x: x['username']), 1):
                        f.write(f"{i}. {item['username']}\n")
                else:
                    f.write("Everyone you follow also follows you back!\n")
                f.write("\n")
                
                # Write accounts you don't follow back
                f.write("=== ACCOUNTS YOU DON'T FOLLOW BACK ===\n")
                if self.you_dont_follow:
                    for i, item in enumerate(sorted(self.you_dont_follow, key=lambda x: x['username']), 1):
                        f.write(f"{i}. {item['username']}\n")
                else:
                    f.write("You follow everyone who follows you!\n")
                f.write("\n")
                
                # Write mutual connections
                f.write("=== MUTUAL CONNECTIONS ===\n")
                if self.mutual:
                    for i, item in enumerate(sorted(self.mutual, key=lambda x: x['username']), 1):
                        f.write(f"{i}. {item['username']}\n")
                else:
                    f.write("No mutual connections found.\n")
                
            messagebox.showinfo("Report Saved", f"Report saved to {filepath}")
            
            # Try to open the report
            try:
                os.startfile(filepath)
            except:
                pass
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {e}")

if __name__ == "__main__":
    root = tk.Tk()
    app = InstagramJSONAnalyzer(root)
    root.mainloop()
