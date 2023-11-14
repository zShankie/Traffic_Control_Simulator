import tkinter as tk
from tkinter import ttk
import threading
import random
import time


class TrafficSimulator:
    def __init__(self, root):
        self.root = root
        self.root.title("Traffic Simulator")
        self.canvas_width = 800
        self.canvas_height = 600
        self.canvas = tk.Canvas(self.root, width=self.canvas_width, height=self.canvas_height)
        self.canvas.pack()

        # Background
        self.canvas.create_rectangle(0, 0, self.canvas_width, self.canvas_height, fill="lightgray", outline="lightgray")

        # Roads
        self.draw_roads()

        # Vehicles
        self.vehicles = []
        self.generate_vehicles()

        # Traffic Signals
        self.signal_coordinates = [(self.canvas_width // 2 - 40, 100),
                                   (self.canvas_width // 2 - 40, 200),
                                   (self.canvas_width // 2 - 40, 300),
                                   (self.canvas_width // 2 - 40, 400)]

        self.signal_colors = ["red", "red", "red", "red"]
        self.draw_signals()

        # Control Panel
        self.setup_control_panel()

    def draw_roads(self):
        road_color = "gray"
        road_width = 400
        self.canvas.create_rectangle(self.canvas_width // 2 - road_width // 2, 0,
                                     self.canvas_width // 2 + road_width // 2, self.canvas_height,
                                     fill=road_color)

    def generate_vehicles(self):
        for i in range(5):
            x = random.randint(100, self.canvas_width - 100)
            y = random.randint(0, self.canvas_height - 50)
            vehicle = self.canvas.create_rectangle(x, y, x + 50, y + 30, fill="gray", tags="vehicle")
            self.vehicles.append(vehicle)

    def draw_signals(self):
        for i, color in enumerate(self.signal_colors):
            x, y = self.signal_coordinates[i]
            self.canvas.create_oval(x, y, x + 40, y + 40, fill=color, tags="signal")

    def setup_control_panel(self):
        control_panel = ttk.Frame(self.root)
        control_panel.pack(pady=10)

        start_button = ttk.Button(control_panel, text="Start Simulation", command=self.start_simulation)
        start_button.grid(row=0, column=0, padx=10)

        stop_button = ttk.Button(control_panel, text="Stop Simulation", command=self.stop_simulation)
        stop_button.grid(row=0, column=1, padx=10)

        self.root.protocol("WM_DELETE_WINDOW", self.on_close)

        self.is_simulation_running = False
        self.simulation_thread = None
        self.stop_event = threading.Event()

    def start_simulation(self):
        if not self.is_simulation_running:
            self.is_simulation_running = True
            self.stop_event.clear()  # Clear the event before starting a new simulation
            self.simulation_thread = threading.Thread(target=self.simulation_loop)
            self.simulation_thread.start()

    def stop_simulation(self):
        self.is_simulation_running = False
        if self.simulation_thread:
            # Signal the thread to stop
            self.stop_event.set()
            # Wait for the thread to finish (with a timeout)
            self.simulation_thread.join(timeout=1)

    def simulation_loop(self):
        while not self.stop_event.is_set():
            time.sleep(1)
            self.update_signals()
            self.move_vehicles()

    def update_signals(self):
        # Update signals independently
        for i in range(4):
            if random.random() < 0.5:
                self.signal_colors[i] = "red"
            else:
                self.signal_colors[i] = "green"

        self.canvas.delete("signal")
        self.draw_signals()

        # Change the color of vehicles based on their corresponding signal state
        for i, vehicle in enumerate(self.vehicles):
            signal_state = self.signal_colors[i % 4]  # Use modulo to cycle through signal states
            vehicle_color = "red" if signal_state == "red" else "green"
            self.canvas.itemconfig(vehicle, fill=vehicle_color)

    def move_vehicles(self):
        for vehicle in self.vehicles:
            speed = random.randint(2, 5)
            x, y, _, _ = self.canvas.coords(vehicle)
            if x + speed < self.canvas_width:
                self.canvas.move(vehicle, speed, 0)
            else:
                self.canvas.move(vehicle, -self.canvas_width, 0)
            self.canvas.update()

    def on_close(self):
        self.stop_simulation()
        self.root.destroy()


if __name__ == "__main__":
    root = tk.Tk()
    app = TrafficSimulator(root)
    root.mainloop()

#End of Source Code
