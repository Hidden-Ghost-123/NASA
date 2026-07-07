import tkinter as tk
from tkinter import ttk
import random
import time

class NasaDashboard(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("NASA - DEEP SPACE MONITORING MATRIX v4.2.6")
        self.geometry("1100x700")
        self.configure(bg="#0a0f1d")

        # Color Palette
        self.bg_dark = "#0a0f1d"
        self.bg_panel = "#111827"
        self.accent_cyan = "#00f0ff"
        self.accent_green = "#39ff14"
        self.accent_red = "#ff3333"
        self.text_white = "#e2e8f0"
        self.text_muted = "#64748b"

        # Mock Data State Variables
        self.iss_lat = 45.1234
        self.iss_lon = -120.5678
        
        # Configure Styles
        self.setup_styles()
        
        # Build UI layout
        self.create_header()
        self.create_main_layout()
        
        self.update_iss_stream()
        self.update_solar_telemetry()

    def setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")
        
        # Notebook/Tabs styling
        style.configure("TNotebook", background=self.bg_dark, borderwidth=0)
        style.configure("TNotebook.Tab", background=self.bg_panel, foreground=self.text_muted, 
                        padding=[15, 5], font=("Consolas", 10, "bold"), borderwidth=0)
        style.map("TNotebook.Tab", background=[("selected", self.accent_cyan)], 
                  foreground=[("selected", self.bg_dark)])
        
        # Treeview styling (Asteroid table)
        style.configure("Treeview", background=self.bg_panel, fieldbackground=self.bg_panel, 
                        foreground=self.text_white, rowheight=25, font=("Consolas", 10))
        style.configure("Treeview.Heading", background=self.bg_dark, foreground=self.accent_cyan, 
                        font=("Consolas", 10, "bold"))
        style.map("Treeview", background=[("selected", "#1e293b")])

    def create_header(self):
        header_frame = tk.Frame(self, bg=self.bg_panel, height=60, bd=1, relief="groove")
        header_frame.pack(fill="x", side="top", padx=10, pady=10)
        header_frame.pack_propagate(False)

        title_lbl = tk.Label(header_frame, text="🚀 NASA LIVE DATA SIMULATION NETWORK", 
                             font=("Consolas", 16, "bold"), bg=self.bg_panel, fg=self.accent_cyan)
        title_lbl.pack(side="left", padx=15, pady=12)

        status_lbl = tk.Label(header_frame, text="SYSTEM STATUS: ONLINE // API MOCK MODE", 
                              font=("Consolas", 10), bg=self.bg_panel, fg=self.accent_green)
        status_lbl.pack(side="right", padx=15, pady=15)

    def create_main_layout(self):
        # Notebook container for multi-panel views
        notebook = ttk.Notebook(self)
        notebook.pack(fill="both", expand=True, padx=10, pady=(0, 10))

        # Initialize Frames
        tab_apod = tk.Frame(notebook, bg=self.bg_dark)
        tab_asteroids = tk.Frame(notebook, bg=self.bg_dark)
        tab_iss = tk.Frame(notebook, bg=self.bg_dark)
        tab_mars = tk.Frame(notebook, bg=self.bg_dark)
        tab_weather = tk.Frame(notebook, bg=self.bg_dark)

        notebook.add(tab_apod, text="🌌 DAILY APOD")
        notebook.add(tab_asteroids, text="☄️ ASTEROID TRACKER")
        notebook.add(tab_iss, text="🛰️ ISS REAL-TIME")
        notebook.add(tab_mars, text="🔴 MARS ROVER")
        notebook.add(tab_weather, text="☀️ SOLAR WEATHER")

        self.build_apod_module(tab_apod)
        self.build_asteroid_module(tab_asteroids)
        self.build_iss_module(tab_iss)
        self.build_mars_module(tab_mars)
        self.build_weather_module(tab_weather)

    def build_apod_module(self, parent):
        panel = tk.Frame(parent, bg=self.bg_panel, bd=1, relief="solid")
        panel.pack(fill="both", expand=True, padx=20, pady=20)

        title = tk.Label(panel, text="Astronomy Picture of the Day: The Pillars of Creation", 
                         font=("Consolas", 14, "bold"), bg=self.bg_panel, fg=self.accent_cyan)
        title.pack(anchor="w", padx=20, pady=15)

        # Image placeholder mimicking graphical visual data
        img_canvas = tk.Canvas(panel, width=400, height=250, bg="#0d1527", highlightthickness=1, highlightbackground=self.accent_cyan)
        img_canvas.pack(side="left", padx=20, pady=10, fill="both", expand=True)
        img_canvas.create_text(200, 125, text="[MOCK HD APOD IMAGE FRAME]\n(pillars_of_creation_jwst.png)", 
                               fill=self.text_muted, font=("Consolas", 11), justify="center")

        # Description text
        desc_frame = tk.Frame(panel, bg=self.bg_panel)
        desc_frame.pack(side="right", fill="both", expand=True, padx=20, pady=10)

        meta_lbl = tk.Label(desc_frame, text="Date: 2026-07-07 | Copyright: JWST Science Team", 
                            font=("Consolas", 10, "italic"), bg=self.bg_panel, fg=self.accent_green)
        meta_lbl.pack(anchor="w", pady=(0, 10))

        explanation = (
            "This striking image captured by the James Webb Space Telescope reveals near infrared "
            "details of the Pillars of Creation. New stars are forming inside these dense clouds of "
            "gas and dust. The three-dimensional pillars look like majestic rock formations, but are "
            "composed of cool interstellar gas and dust that appear semi-transparent in near infrared light."
        )
        desc_text = tk.Text(desc_frame, bg=self.bg_panel, fg=self.text_white, wrap="word", 
                            font=("Helvetica", 11), bd=0, highlightthickness=0)
        desc_text.insert("1.0", explanation)
        desc_text.config(state="disabled")
        desc_text.pack(fill="both", expand=True)

    def build_asteroid_module(self, parent):
        title = tk.Label(parent, text="⚠️ NEAR-EARTH OBJECT (NEO) CLOSE APPROACHES", 
                         font=("Consolas", 12, "bold"), bg=self.bg_dark, fg=self.accent_cyan)
        title.pack(anchor="w", padx=20, pady=10)

        # Treeview grid
        columns = ("name", "velocity", "miss_dist", "diameter", "danger_score")
        self.neo_tree = ttk.Treeview(parent, columns=columns, show="headings")
        
        self.neo_tree.heading("name", text="Object Name")
        self.neo_tree.heading("velocity", text="Velocity (km/h)")
        self.neo_tree.heading("miss_dist", text="Miss Distance (km)")
        self.neo_tree.heading("diameter", text="Est. Diameter (m)")
        self.neo_tree.heading("danger_score", text="Danger Score (0-100)")

        self.neo_tree.column("name", width=150, anchor="center")
        self.neo_tree.column("velocity", width=150, anchor="center")
        self.neo_tree.column("miss_dist", width=180, anchor="center")
        self.neo_tree.column("diameter", width=150, anchor="center")
        self.neo_tree.column("danger_score", width=150, anchor="center")

        self.neo_tree.pack(fill="both", expand=True, padx=20, pady=10)

        # Custom Danger Score Calculation Engine & Mock Data Injector
        mock_asteroids = [
            {"name": "Asteroid 2026-AM4", "vel": 45200, "dist": 1200000, "dia": 140},
            {"name": "Apophis 99942", "vel": 107000, "dist": 38000, "dia": 370},
            {"name": "Neo-X-Lightweight", "vel": 22000, "dist": 6400000, "dia": 12},
            {"name": "Bennu B-Type", "vel": 63000, "dist": 4200000, "dia": 490},
            {"name": "Comet Shadow-01", "vel": 89000, "dist": 850000, "dia": 1200}
        ]

        for ast in mock_asteroids:
            score = int((ast["dia"] * 150) / (ast["dist"] / 10000))
            score = min(max(score, 1), 99) # Keep scaled tightly between 1-99
            
            status = f"{score} - ALERT" if score > 70 else f"{score} - NOMINAL"
            
            self.neo_tree.insert("", "end", values=(
                ast["name"], 
                f"{ast['vel']:,}", 
                f"{ast['dist']:,}", 
                ast["dia"], 
                status
            ))

    def build_iss_module(self, parent):
        main_frame = tk.Frame(parent, bg=self.bg_panel, bd=1, relief="solid")
        main_frame.pack(fill="both", expand=True, padx=20, pady=20)

        # Left Readout Controls
        readout_frame = tk.Frame(main_frame, bg=self.bg_panel)
        readout_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(readout_frame, text="INTERNATIONAL SPACE STATION TELEMETRY", 
                 font=("Consolas", 14, "bold"), bg=self.bg_panel, fg=self.accent_cyan).pack(anchor="w", pady=10)

        self.lat_lbl = tk.Label(readout_frame, text="LATITUDE:  0.0000°", font=("Consolas", 20), bg=self.bg_panel, fg=self.text_white)
        self.lat_lbl.pack(anchor="w", pady=10)

        self.lon_lbl = tk.Label(readout_frame, text="LONGITUDE: 0.0000°", font=("Consolas", 20), bg=self.bg_panel, fg=self.text_white)
        self.lon_lbl.pack(anchor="w", pady=10)

        self.alt_lbl = tk.Label(readout_frame, text="ALTITUDE:  418.42 km", font=("Consolas", 12), bg=self.bg_panel, fg=self.accent_green)
        self.alt_lbl.pack(anchor="w", pady=5)

        self.vel_lbl = tk.Label(readout_frame, text="ORBITAL VELOCITY: 27,560 km/h", font=("Consolas", 12), bg=self.bg_panel, fg=self.accent_green)
        self.vel_lbl.pack(anchor="w", pady=5)

        self.map_canvas = tk.Canvas(main_frame, width=450, height=250, bg="#070b12", highlightthickness=1, highlightbackground=self.accent_cyan)
        self.map_canvas.pack(side="right", padx=20, pady=20, fill="both", expand=True)
        self.draw_orbital_grid()

    def draw_orbital_grid(self):
        self.map_canvas.delete("grid")
        # Draw some decorative green cyber-grid lines mimicking a tracking map
        for i in range(0, 500, 40):
            self.map_canvas.create_line(i, 0, i, 300, fill="#13233c", tags="grid")
            self.map_canvas.create_line(0, i, 500, i, fill="#13233c", tags="grid")
        self.map_canvas.create_text(225, 140, text="🌍 LIVE GROUND TRACK MATRIX", fill="#22395d", font=("Consolas", 14, "bold"), tags="grid")

    def update_iss_stream(self):
        self.iss_lat += random.uniform(-0.15, 0.15)
        self.iss_lon += random.uniform(0.1, 0.3)

        # Keep values wrapped around coordinates constraints
        if self.iss_lat > 90 or self.iss_lat < -90: self.iss_lat *= -1
        if self.iss_lon > 180: self.iss_lon = -180

        self.lat_lbl.config(text=f"LATITUDE:  {self.iss_lat:.4f}°")
        self.lon_lbl.config(text=f"LONGITUDE: {self.iss_lon:.4f}°")

        # Redraw position node point on cyber grid map layout
        self.map_canvas.delete("node")
        x = ((self.iss_lon + 180) / 360) * 450
        y = ((90 - self.iss_lat) / 180) * 250
        self.map_canvas.create_oval(x-6, y-6, x+6, y+6, fill=self.accent_red, outline=self.text_white, tags="node")
        self.map_canvas.create_text(x, y-15, text="ISS NODE", fill=self.accent_cyan, font=("Consolas", 8, "bold"), tags="node")

        self.after(1000, self.update_iss_stream)

    def build_mars_module(self, parent):
        controls = tk.Frame(parent, bg=self.bg_panel, height=60)
        controls.pack(fill="x", side="top", padx=20, pady=10)

        tk.Label(controls, text="Select Rover:", font=("Consolas", 10, "bold"), bg=self.bg_panel, fg=self.text_white).pack(side="left", padx=10)
        
        rover_box = ttk.Combobox(controls, values=["Perseverance", "Curiosity", "Opportunity"], state="readonly")
        rover_box.set("Perseverance")
        rover_box.pack(side="left", padx=5)

        tk.Label(controls, text="Select Camera:", font=("Consolas", 10, "bold"), bg=self.bg_panel, fg=self.text_white).pack(side="left", padx=10)
        cam_box = ttk.Combobox(controls, values=["NAVCAM (Navigation Camera)", "MASTCAM", "HAZCAM (Hazard Avoidance)"], state="readonly")
        cam_box.set("NAVCAM (Navigation Camera)")
        cam_box.pack(side="left", padx=5)

        query_btn = tk.Button(controls, text="QUERY ROVER DB", bg=self.accent_cyan, fg=self.bg_dark, 
                              font=("Consolas", 9, "bold"), activebackground=self.text_white, bd=0, padx=10)
        query_btn.pack(side="left", padx=15)

        # Grid view display container
        photo_grid = tk.Frame(parent, bg=self.bg_dark)
        photo_grid.pack(fill="both", expand=True, padx=20, pady=10)

        for i in range(3):
            card = tk.Frame(photo_grid, bg=self.bg_panel, bd=1, relief="solid", width=220)
            card.pack(side="left", fill="both", expand=True, padx=5, pady=5)
            card.pack_propagate(False)

            # Mock Photo display square box
            box = tk.Canvas(card, bg="#1a2333", highlightthickness=0)
            box.pack(fill="both", expand=True, padx=10, pady=10)
            box.create_text(110, 75, text="📸 MARS RAW DATA\nIMAGE VIEW", fill=self.text_muted, font=("Consolas", 10), justify="center")

            lbl_sol = tk.Label(card, text=f"Sol: {1240 + (i*14)}", font=("Consolas", 10), bg=self.bg_panel, fg=self.accent_green)
            lbl_sol.pack(anchor="w", padx=10)
            
            lbl_id = tk.Label(card, text=f"ID Ref: IMG_0984124{i}9-NASA", font=("Consolas", 8), bg=self.bg_panel, fg=self.text_muted)
            lbl_id.pack(anchor="w", padx=10, pady=(0, 10))

    def build_weather_module(self, parent):
        # Left Panel - Telemetry Gauges
        gauge_frame = tk.Frame(parent, bg=self.bg_panel, bd=1, relief="solid")
        gauge_frame.pack(side="left", fill="both", expand=True, padx=20, pady=20)

        tk.Label(gauge_frame, text="DONKI SPACE WEATHER FEED", font=("Consolas", 12, "bold"), bg=self.bg_panel, fg=self.accent_cyan).pack(anchor="w", padx=15, pady=10)

        self.solar_flare_lbl = tk.Label(gauge_frame, text="SOLAR WIND FLUX: 412.8 km/s", font=("Consolas", 11), bg=self.bg_panel, fg=self.text_white)
        self.solar_flare_lbl.pack(anchor="w", padx=15, pady=8)

        self.geomag_lbl = tk.Label(gauge_frame, text="GEOMAGNETIC Kp-INDEX: 3 (NORMAL)", font=("Consolas", 11), bg=self.bg_panel, fg=self.accent_green)
        self.geomag_lbl.pack(anchor="w", padx=15, pady=8)

        # Right Panel - Live Ticker Feed Log
        log_frame = tk.Frame(parent, bg=self.bg_panel, bd=1, relief="solid")
        log_frame.pack(side="right", fill="both", expand=True, padx=(0, 20), pady=20)

        tk.Label(log_frame, text="INCIDENT REALTIME MONITOR LOG", font=("Consolas", 10, "bold"), bg=self.bg_panel, fg=self.text_muted).pack(anchor="w", padx=15, pady=5)

        self.log_box = tk.Text(log_frame, bg="#070b11", fg=self.accent_green, font=("Consolas", 9), bd=0, highlightthickness=1, highlightbackground="#1e293b")
        self.log_box.pack(fill="both", expand=True, padx=15, pady=10)
        
        # Populate initial terminal log records
        self.log_box.insert("end", "[02:14:05 UTC] - SYSTEM INIT: Standing by for solar activity feeds.\n")
        self.log_box.insert("end", "[03:45:12 UTC] - DATA: Coronal Mass Ejection (CME) analyzed. Vector offset outside Earth impact arc.\n")
        self.log_box.config(state="disabled")

    def update_solar_telemetry(self):
        wind_speed = round(random.uniform(380.0, 650.5), 1)
        kp_index = random.randint(1, 9)
        
        self.solar_flare_lbl.config(text=f"SOLAR WIND FLUX: {wind_speed} km/s")
        
        kp_status = "NORMAL" if kp_index < 4 else "MODERATE STORM" if kp_index < 7 else "SEVERE GEOMAGNETIC DISRUPTION"
        kp_color = self.accent_green if kp_index < 4 else "orange" if kp_index < 7 else self.accent_red
        
        self.geomag_lbl.config(text=f"GEOMAGNETIC Kp-INDEX: {kp_index} ({kp_status})", fg=kp_color)

        if random.random() > 0.75:
            self.log_box.config(state="normal")
            current_time = time.strftime("%H:%M:%S")
            alert_class = random.choice(["C-Class", "M-Class", "X-Class (High Severity)"])
            self.log_box.insert("end", f"[{current_time} UTC] - TELEMETRY EVENT: Solar Flare event of class {alert_class} caught by SOHO instruments.\n")
            self.log_box.see("end")
            self.log_box.config(state="disabled")

        self.after(3000, self.update_solar_telemetry)

if __name__ == "__main__":
    app = NasaDashboard()
    app.mainloop()
