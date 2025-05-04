import os
import sys
import csv
import tkinter as tk
from tkinter import ttk, filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import threading
from datetime import datetime
from bs4 import BeautifulSoup
import webbrowser

# Define constants
DATA_FOLDER = "data_of_instagram"
REPORTS_FOLDER = "reports"

# Create folders if they don't exist
for folder in [DATA_FOLDER, REPORTS_FOLDER]:
    if not os.path.exists(folder):
        os.makedirs(folder)

class InstagramAnalyzerApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Instagram Follower Analyzer 🔍")
        self.root.geometry("900x650")
        self.root.minsize(800, 600)
        
        # Set app icon if available
        try:
            self.root.iconbitmap("instagram_icon.ico")
        except:
            pass
        
        # Variables
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
        
        # Set theme colors
        self.bg_color = "#f5f5f5"
        self.accent_color = "#E1306C"  # Instagram pink
        self.secondary_color = "#405DE6"  # Instagram blue
        self.text_color = "#262626"
        
        self.root.configure(bg=self.bg_color)
        
        # Create styles
        self.style = ttk.Style()
        self.style.configure("TFrame", background=self.bg_color)
        self.style.configure("Header.TLabel", 
                             font=("Helvetica", 16, "bold"), 
                             background=self.bg_color, 
                             foreground=self.text_color)
        self.style.configure("Stats.TLabel", 
                             font=("Helvetica", 14), 
                             background=self.bg_color, 
                             foreground=self.text_color)
        self.style.configure("Accent.TButton", 
                             font=("Helvetica", 12, "bold"),
                             background=self.accent_color)
        
        # Main layout
        self.create_widgets()
        
        # Check if data files already exist
        self._check_existing_data()
    
    def create_widgets(self):
        # Main container
        main_frame = ttk.Frame(self.root, padding="20")
        main_frame.pack(fill=tk.BOTH, expand=True)
        
        # Title
        title_frame = ttk.Frame(main_frame)
        title_frame.pack(fill=tk.X, pady=(0, 20))
        
        title_label = ttk.Label(title_frame, text="Instagram Follower Analyzer 🔍", 
                                font=("Helvetica", 20, "bold"), 
                                foreground=self.accent_color, 
                                background=self.bg_color)
        title_label.pack(side=tk.LEFT)
        
        # File selection frame
        file_frame = ttk.LabelFrame(main_frame, text="Step 1: Select Instagram Data Files", padding=10)
        file_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Following file
        ttk.Label(file_frame, text="Following HTML File:").grid(row=0, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.following_file, width=50).grid(row=0, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse...", command=lambda: self._browse_file(self.following_file)).grid(row=0, column=2, padx=5, pady=5)
        
        # Followers file
        ttk.Label(file_frame, text="Followers HTML File:").grid(row=1, column=0, sticky=tk.W, pady=5)
        ttk.Entry(file_frame, textvariable=self.followers_file, width=50).grid(row=1, column=1, padx=5, pady=5)
        ttk.Button(file_frame, text="Browse...", command=lambda: self._browse_file(self.followers_file)).grid(row=1, column=2, padx=5, pady=5)
        
        # Action buttons
        action_frame = ttk.Frame(main_frame)
        action_frame.pack(fill=tk.X, pady=(0, 10))
        
        analyze_btn = ttk.Button(action_frame, text="Analyze Data", command=self.analyze_data, style="Accent.TButton")
        analyze_btn.pack(side=tk.LEFT, padx=(0, 10))
        
        save_report_btn = ttk.Button(action_frame, text="Save Full Report", command=self.save_report)
        save_report_btn.pack(side=tk.LEFT)
        
        # Results notebook (tabbed view)
        self.notebook = ttk.Notebook(main_frame)
        self.notebook.pack(fill=tk.BOTH, expand=True)
        
        # Summary tab
        summary_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(summary_frame, text="Summary")
        
        # Stats frame
        stats_frame = ttk.LabelFrame(summary_frame, text="Statistics", padding=10)
        stats_frame.pack(fill=tk.X, pady=(0, 10))
        
        # Statistics grid
        ttk.Label(stats_frame, text="Following:").grid(row=0, column=0, sticky=tk.W, pady=2)
        ttk.Label(stats_frame, textvariable=self.following_count, font=("Helvetica", 12, "bold")).grid(row=0, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(stats_frame, text="Followers:").grid(row=1, column=0, sticky=tk.W, pady=2)
        ttk.Label(stats_frame, textvariable=self.followers_count, font=("Helvetica", 12, "bold")).grid(row=1, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(stats_frame, text="Mutual Connections:").grid(row=2, column=0, sticky=tk.W, pady=2)
        ttk.Label(stats_frame, textvariable=self.mutual_count, font=("Helvetica", 12, "bold")).grid(row=2, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(stats_frame, text="Not Following You Back:").grid(row=3, column=0, sticky=tk.W, pady=2)
        ttk.Label(stats_frame, textvariable=self.not_following_back_count, font=("Helvetica", 12, "bold")).grid(row=3, column=1, sticky=tk.W, pady=2)
        
        ttk.Label(stats_frame, text="You Don't Follow Back:").grid(row=4, column=0, sticky=tk.W, pady=2)
        ttk.Label(stats_frame, textvariable=self.you_dont_follow_count, font=("Helvetica", 12, "bold")).grid(row=4, column=1, sticky=tk.W, pady=2)
        
        # Chart frame (placeholder for potential future chart)
        chart_frame = ttk.Frame(summary_frame)
        chart_frame.pack(fill=tk.BOTH, expand=True)
        
        # Donut chart canvas (simple visualization)
        self.canvas = tk.Canvas(chart_frame, bg="white", height=300)
        self.canvas.pack(fill=tk.BOTH, expand=True)
        
        # Create other tabs for detailed list views
        # Not following back tab
        self.not_following_back_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.not_following_back_frame, text="Not Following You Back 💔")
        
        self.not_following_back_treeview = self._create_profile_treeview(self.not_following_back_frame)
        
        # You don't follow tab
        self.you_dont_follow_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.you_dont_follow_frame, text="You Don't Follow Back 🤔")
        
        self.you_dont_follow_treeview = self._create_profile_treeview(self.you_dont_follow_frame)
        
        # Mutual connections tab
        self.mutual_frame = ttk.Frame(self.notebook, padding=10)
        self.notebook.add(self.mutual_frame, text="Mutual Connections 👍")
        
        self.mutual_treeview = self._create_profile_treeview(self.mutual_frame)
        
        # Footer
        footer_frame = ttk.Frame(main_frame)
        footer_frame.pack(fill=tk.X, pady=(10, 0))
        
        status_label = ttk.Label(footer_frame, text="Ready. Select your Instagram data files to begin.")
        status_label.pack(side=tk.LEFT)
        
        # Set this as the status label for updating
        self.status_label = status_label
    
    def _create_profile_treeview(self, parent):
        # Create a treeview with scrollbar
        frame = ttk.Frame(parent)
        frame.pack(fill=tk.BOTH, expand=True)
        
        # Create the treeview
        columns = ("username", "profile_url", "date_info")
        treeview = ttk.Treeview(frame, columns=columns, show="headings")
        treeview.heading("username", text="Username")
        treeview.heading("profile_url", text="Profile URL")
        treeview.heading("date_info", text="Date")
        
        treeview.column("username", width=150)
        treeview.column("profile_url", width=250)
        treeview.column("date_info", width=150)
        
        # Add scrollbars
        vsb = ttk.Scrollbar(frame, orient="vertical", command=treeview.yview)
        hsb = ttk.Scrollbar(frame, orient="horizontal", command=treeview.xview)
        treeview.configure(yscrollcommand=vsb.set, xscrollcommand=hsb.set)
        
        # Grid layout for treeview and scrollbars
        treeview.grid(column=0, row=0, sticky="nsew")
        vsb.grid(column=1, row=0, sticky="ns")
        hsb.grid(column=0, row=1, sticky="ew")
        
        # Configure grid weights
        frame.columnconfigure(0, weight=1)
        frame.rowconfigure(0, weight=1)
        
        # Double-click to open profile
        treeview.bind("<Double-1>", self._on_profile_double_click)
        
        return treeview
    
    def _on_profile_double_click(self, event):
        # Get the treeview that was clicked
        treeview = event.widget
        
        # Get the selected item
        selection = treeview.selection()
        if selection:
            # Get the profile URL from the selected item
            item = treeview.item(selection[0])
            profile_url = item["values"][1]
            
            # Open the URL in the default web browser
            if profile_url:
                webbrowser.open(profile_url)
    
    def _browse_file(self, string_var):
        filename = filedialog.askopenfilename(
            filetypes=[("HTML Files", "*.html"), ("All Files", "*.*")]
        )
        if filename:
            string_var.set(filename)
    
    def _check_existing_data(self):
        # Check if HTML files exist in data folder
        following_path = os.path.join(DATA_FOLDER, "following.html")
        followers_path = os.path.join(DATA_FOLDER, "followers_1.html")
        
        if os.path.exists(following_path):
            self.following_file.set(following_path)
        
        if os.path.exists(followers_path):
            self.followers_file.set(followers_path)
        
        # If both files exist, offer to analyze
        if os.path.exists(following_path) and os.path.exists(followers_path):
            if messagebox.askyesno("Files Found", 
                                "Instagram data files found in the data folder. Would you like to analyze them now?"):
                self.analyze_data()
    
    def _update_status(self, message):
        self.status_label.config(text=message)
        self.root.update_idletasks()
    
    def _draw_chart(self):
        # Clear canvas
        self.canvas.delete("all")
        
        # Get counts
        following = self.following_count.get()
        followers = self.followers_count.get()
        mutual = self.mutual_count.get()
        not_following_back = self.not_following_back_count.get()
        you_dont_follow = self.you_dont_follow_count.get()
        
        if following == 0 and followers == 0:
            self.canvas.create_text(
                self.canvas.winfo_width() // 2, 
                self.canvas.winfo_height() // 2,
                text="No data available for visualization",
                font=("Helvetica", 14),
                fill="gray"
            )
            return
        
        # Draw a simple donut chart
        cx = self.canvas.winfo_width() // 2
        cy = self.canvas.winfo_height() // 2
        r_outer = min(cx, cy) - 50
        r_inner = r_outer - 40
        
        # Mutual connections (green)
        self._draw_donut_segment(cx, cy, r_inner, r_outer, 0, 360 * mutual / max(following, followers), "#4CAF50")
        
        # Not following back (red)
        self._draw_donut_segment(cx, cy, r_inner, r_outer, 
                                360 * mutual / max(following, followers), 
                                360 * (mutual + not_following_back) / max(following, followers), 
                                "#F44336")
        
        # You don't follow (blue)
        self._draw_donut_segment(cx, cy, r_inner, r_outer, 
                                360 * (mutual + not_following_back) / max(following, followers), 
                                360, 
                                "#2196F3")
        
        # Add legend
        legend_x = 10
        legend_y = 10
        legend_spacing = 25
        
        # Mutual
        self.canvas.create_rectangle(legend_x, legend_y, legend_x + 20, legend_y + 20, fill="#4CAF50", outline="")
        self.canvas.create_text(legend_x + 25, legend_y + 10, text=f"Mutual Connections ({mutual})", anchor="w")
        
        # Not following back
        self.canvas.create_rectangle(legend_x, legend_y + legend_spacing, legend_x + 20, legend_y + legend_spacing + 20, 
                                    fill="#F44336", outline="")
        self.canvas.create_text(legend_x + 25, legend_y + legend_spacing + 10, 
                                text=f"Not Following You Back ({not_following_back})", anchor="w")
        
        # You don't follow
        self.canvas.create_rectangle(legend_x, legend_y + 2 * legend_spacing, legend_x + 20, legend_y + 2 * legend_spacing + 20, 
                                    fill="#2196F3", outline="")
        self.canvas.create_text(legend_x + 25, legend_y + 2 * legend_spacing + 10, 
                                text=f"You Don't Follow Back ({you_dont_follow})", anchor="w")
    
    def _draw_donut_segment(self, cx, cy, r_inner, r_outer, start_angle, end_angle, fill_color):
        if start_angle >= end_angle:
            return
        
        # Convert angles to radians and adjust for tkinter's coordinate system
        import math
        start_angle = math.radians(90 - start_angle)
        end_angle = math.radians(90 - end_angle)
        
        # Calculate points
        x_outer_start = cx + r_outer * math.cos(start_angle)
        y_outer_start = cy - r_outer * math.sin(start_angle)
        x_outer_end = cx + r_outer * math.cos(end_angle)
        y_outer_end = cy - r_outer * math.sin(end_angle)
        
        x_inner_start = cx + r_inner * math.cos(start_angle)
        y_inner_start = cy - r_inner * math.sin(start_angle)
        x_inner_end = cx + r_inner * math.cos(end_angle)
        y_inner_end = cy - r_inner * math.sin(end_angle)
        
        # Decide which arc type to use based on the angle difference
        angle_diff = (math.degrees(start_angle) - math.degrees(end_angle)) % 360
        large_arc = 1 if angle_diff > 180 else 0
        
        # Create the arc path
        path = [
            (x_outer_start, y_outer_start),
            self.canvas.create_arc(
                cx - r_outer, cy - r_outer, cx + r_outer, cy + r_outer,
                start=math.degrees(start_angle) - 90, extent=math.degrees(end_angle - start_angle),
                style=tk.PIESLICE, outline="", fill=fill_color
            ),
            self.canvas.create_arc(
                cx - r_inner, cy - r_inner, cx + r_inner, cy + r_inner,
                start=math.degrees(start_angle) - 90, extent=math.degrees(end_angle - start_angle),
                style=tk.PIESLICE, outline="", fill=self.bg_color
            )
        ]

    def parse_instagram_html(self, html_file):
        """Parse Instagram HTML file and extract profile data."""
        data = []
        try:
            with open(html_file, 'r', encoding='utf-8') as file:
                content = file.read()
            
            soup = BeautifulSoup(content, 'html.parser')
            
            # Get title for the type of data
            header_title = ""
            header = soup.select_one('h1')
            if header:
                header_title = header.text.strip()
            
            # Find all profile entries
            profile_entries = soup.select('div.pam._3-95._2ph-._a6-g.uiBoxWhite.noborder')
            
            for entry in profile_entries:
                # Get username (from the link)
                username_link = entry.select_one('a')
                if not username_link:
                    continue
                    
                username = username_link.text.strip()
                profile_url = username_link.get('href', '')
                
                # Get date information
                date_div = entry.select_one('div._a6-p > div > div:nth-of-type(2)')
                date_info = date_div.text.strip() if date_div else ""
                
                data.append({
                    'username': username,
                    'profile_url': profile_url,
                    'date_info': date_info
                })
            
            return header_title, data
            
        except Exception as e:
            messagebox.showerror("Error", f"Error parsing HTML file: {e}")
            return "", []
    
    def analyze_data(self):
        """Analyze the Instagram data files."""
        # Get file paths
        following_file = self.following_file.get()
        followers_file = self.followers_file.get()
        
        # Check if files exist
        if not following_file or not os.path.exists(following_file):
            messagebox.showerror("Error", "Following file not found.")
            return
        
        if not followers_file or not os.path.exists(followers_file):
            messagebox.showerror("Error", "Followers file not found.")
            return
        
        # Update status
        self._update_status("Analyzing Instagram data files...")
        
        # Run analysis in a separate thread
        threading.Thread(target=self._run_analysis, args=(following_file, followers_file)).start()
    
    def _run_analysis(self, following_file, followers_file):
        # Parse following file
        following_title, following_data = self.parse_instagram_html(following_file)
        self.following_data = following_data
        
        # Parse followers file
        followers_title, followers_data = self.parse_instagram_html(followers_file)
        self.followers_data = followers_data
        
        # Extract usernames
        following_usernames = set(item['username'] for item in following_data)
        followers_usernames = set(item['username'] for item in followers_data)
        
        # Calculate relationships
        mutual_usernames = following_usernames.intersection(followers_usernames)
        not_following_back_usernames = following_usernames - followers_usernames
        you_dont_follow_usernames = followers_usernames - following_usernames
        
        # Update counts
        self.following_count.set(len(following_usernames))
        self.followers_count.set(len(followers_usernames))
        self.mutual_count.set(len(mutual_usernames))
        self.not_following_back_count.set(len(not_following_back_usernames))
        self.you_dont_follow_count.set(len(you_dont_follow_usernames))
        
        # Filter data by username sets
        self.mutual = [item for item in following_data if item['username'] in mutual_usernames]
        self.not_following_back = [item for item in following_data if item['username'] in not_following_back_usernames]
        self.you_dont_follow = [item for item in followers_data if item['username'] in you_dont_follow_usernames]
        
        # Update UI from the main thread
        self.root.after(0, self._update_ui_with_results)
    
    def _update_ui_with_results(self):
        # Clear existing entries in treeviews
        for treeview in [self.not_following_back_treeview, self.you_dont_follow_treeview, self.mutual_treeview]:
            for i in treeview.get_children():
                treeview.delete(i)
        
        # Add entries to not following back treeview
        for item in self.not_following_back:
            self.not_following_back_treeview.insert("", "end", values=(
                item['username'], item['profile_url'], item['date_info']
            ))
        
        # Add entries to you don't follow treeview
        for item in self.you_dont_follow:
            self.you_dont_follow_treeview.insert("", "end", values=(
                item['username'], item['profile_url'], item['date_info']
            ))
        
        # Add entries to mutual treeview
        for item in self.mutual:
            self.mutual_treeview.insert("", "end", values=(
                item['username'], item['profile_url'], item['date_info']
            ))
        
        # Draw chart
        self._draw_chart()
        
        # Update status
        self._update_status(f"Analysis complete. Found {self.not_following_back_count.get()} accounts not following you back.")
        
        # Switch to the tab with not following back accounts
        self.notebook.select(1)
    
    def save_report(self):
        """Save a comprehensive report to a text file."""
        if not self.following_data or not self.followers_data:
            messagebox.showwarning("Warning", "No data to save. Please analyze data first.")
            return
        
        # Create report filename with timestamp
        timestamp = datetime.now().strftime('%Y-%m-%d_%H-%M-%S')
        report_file = os.path.join(REPORTS_FOLDER, f"instagram_report_{timestamp}.txt")
        
        try:
            with open(report_file, 'w', encoding='utf-8') as file:
                file.write("================================\n")
                file.write("   INSTAGRAM FOLLOWING REPORT   \n")
                file.write("================================\n\n")
                file.write(f"Report generated on: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                
                file.write("=== SUMMARY ===\n")
                file.write(f"Total accounts you're following: {self.following_count.get()}\n")
                file.write(f"Total accounts following you: {self.followers_count.get()}\n")
                file.write(f"Mutual connections: {self.mutual_count.get()}\n")
                file.write(f"Not following you back: {self.not_following_back_count.get()}\n")
                file.write(f"You don't follow them: {self.you_dont_follow_count.get()}\n\n")
                
                # Write accounts that don't follow you back
                file.write("=== ACCOUNTS THAT DON'T FOLLOW YOU BACK ===\n")
                if self.not_following_back:
                    for i, item in enumerate(sorted(self.not_following_back, key=lambda x: x['username']), 1):
                        file.write(f"{i}. {item['username']} - {item['date_info']}\n")
                else:
                    file.write("Everyone you follow also follows you back!\n")
                file.write("\n")
                
                # Write accounts you don't follow back
                file.write("=== ACCOUNTS YOU DON'T FOLLOW BACK ===\n")
                if self.you_dont_follow:
                    for i, item in enumerate(sorted(self.you_dont_follow, key=lambda x: x['username']), 1):
                        file.write(f"{i}. {item['username']} - {item['date_info']}\n")
                else:
                    file.write("You follow everyone who follows you!\n")
                file.write("\n")
                
                # Write mutual connections
                file.write("=== MUTUAL CONNECTIONS ===\n")
                if self.mutual:
                    for i, item in enumerate(sorted(self.mutual, key=lambda x: x['username']), 1):
                        file.write(f"{i}. {item['username']} - {item['date_info']}\n")
                else:
                    file.write("No mutual connections found.\n")
            
            messagebox.showinfo("Success", f"Report saved to {report_file}")
            
            # Try to open the report
            try:
                os.startfile(report_file)
            except:
                pass
                
        except Exception as e:
            messagebox.showerror("Error", f"Failed to save report: {e}")

if __name__ == "__main__":
    # Create the main window
    root = tk.Tk()
    app = InstagramAnalyzerApp(root)
    
    # Start the main loop
    root.mainloop() 