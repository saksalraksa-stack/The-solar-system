import tkinter as tk
from tkinter import ttk
import turtle
import math
import random
import time

# ----------------- Tkinter Setup -----------------
root = tk.Tk()
root.title("Helical Solar System - Enhanced")
root.geometry("1200x800")

# ----------------- Turtle Canvas -----------------
canvas = tk.Canvas(root, width=1000, height=700, bg="black")
canvas.pack(side=tk.LEFT)
screen = turtle.TurtleScreen(canvas)
screen.tracer(0)
screen.bgcolor("black")

# ----------------- Control Panel -----------------
control_frame = ttk.Frame(root)
control_frame.pack(side=tk.RIGHT, fill=tk.Y, padx=10, pady=10)

# Speed control
ttk.Label(control_frame, text="Simulation Speed").pack(pady=5)
speed_var = tk.DoubleVar(value=1.0)
ttk.Scale(control_frame, from_=0.1, to=5.0, variable=speed_var,
          orient=tk.HORIZONTAL, length=180).pack()

# Zoom control
ttk.Label(control_frame, text="Zoom (Orbit Scale)").pack(pady=5)
zoom_var = tk.DoubleVar(value=1.0)
ttk.Scale(control_frame, from_=0.5, to=2.0, variable=zoom_var,
          orient=tk.HORIZONTAL, length=180).pack()

# Trail toggle
show_trails_var = tk.BooleanVar(value=True)
ttk.Checkbutton(control_frame, text="Show Trails", variable=show_trails_var).pack(pady=5)

# Pause/Resume
paused = tk.BooleanVar(value=False)
def toggle_pause():
    paused.set(not paused.get())
pause_btn = ttk.Button(control_frame, text="Pause/Resume", command=toggle_pause)
pause_btn.pack(pady=10)

# Reset Trails
def reset_trails():
    for p in planets:
        p["trail"].clear()
        p["trail_t"].clear()
reset_btn = ttk.Button(control_frame, text="Reset Trails", command=reset_trails)
reset_btn.pack(pady=5)

# Info panel
info_label = tk.Label(control_frame, text="Click a planet to see info",
                      justify="left", bg="black", fg="white", width=35, height=20,
                      font=("Consolas", 9), anchor="nw")
info_label.pack(pady=10, fill=tk.BOTH)

# ----------------- Sun -----------------
sun = turtle.RawTurtle(screen)
sun.shape("circle")
sun.color("yellow")
sun.shapesize(2)
sun.penup()
sun.goto(0, 0)

# ----------------- Sun Tail -----------------
sun_tail = turtle.RawTurtle(screen)
sun_tail.hideturtle()
sun_tail.penup()
sun_tail.color("orange")
sun_trail = []

# ----------------- Stars -----------------
stars = []
for _ in range(150):
    x, y = random.randint(-500, 500), random.randint(-350, 350)
    stars.append([x, y])   # mutable list for movement
star_t = turtle.RawTurtle(screen)
star_t.hideturtle()
star_t.penup()

# ----------------- Planet Data -----------------
planet_data = [
    ("Mercury", "gray", 40, 4.7, 4879,   57900000,   47.4),
    ("Venus", "orange", 70, 3.5, 12104,  108200000,  35.0),
    ("Earth", "blue", 100, 3.0, 12742,  149600000,  29.8),
    ("Mars", "red", 150, 2.4, 6779,   227900000,  24.1),
    ("Jupiter", "brown", 220, 1.3, 139820, 778500000, 13.1),
    ("Saturn", "gold", 280, 1.0, 116460, 1433000000, 9.7),
    ("Uranus", "light blue", 340, 0.7, 50724, 2877000000, 6.8),
    ("Neptune", "purple", 400, 0.5, 49244, 4503000000, 5.4),
]

planets = []
for name, color, radius, speed, diameter, distance, velocity in planet_data:
    t = turtle.RawTurtle(screen)
    t.shape("circle")
    t.color(color)
    t.shapesize(0.6)
    t.penup()

    trail_t = turtle.RawTurtle(screen)  # ✅ Separate turtle for trails
    trail_t.hideturtle()
    trail_t.penup()
    trail_t.color(color)

    label = turtle.RawTurtle(screen)  # ✅ Label turtle only for names
    label.hideturtle()
    label.color("white")
    label.penup()

    planets.append({
        "turtle": t,
        "trail_t": trail_t,
        "label": label,
        "name": name,
        "radius": radius,
        "angle": 0,
        "speed": speed,
        "diameter": diameter,
        "distance": distance,
        "velocity": velocity,
        "trail": []
    })

# ----------------- Moon for Earth -----------------
moon = {
    "turtle": turtle.RawTurtle(screen),
    "angle": 0,
    "speed": 12,
    "radius": 15,
}
moon["turtle"].shape("circle")
moon["turtle"].color("white")
moon["turtle"].shapesize(0.3)
moon["turtle"].penup()

# ----------------- Saturn Rings -----------------
ring_t = turtle.RawTurtle(screen)
ring_t.hideturtle()
ring_t.color("gold")
ring_t.width(1)

# ----------------- Comet -----------------
comet = {
    "turtle": turtle.RawTurtle(screen),
    "x": -500,
    "y": random.randint(-200, 200),
    "speed": 3,
    "trail": []
}
comet["turtle"].shape("circle")
comet["turtle"].color("white")
comet["turtle"].shapesize(0.4)
comet["turtle"].penup()

# ----------------- Simulation Variables -----------------
sun_speed = 40
sun_x = 0
last_time = time.time()

# ----------------- Planet Click Info -----------------
def planet_info(x, y):
    for p in planets:
        px, py = p["turtle"].pos()
        if abs(x - px) < 10 and abs(y - py) < 10:
            info = (f"Planet: {p['name']}\n"
                    f"Diameter: {p['diameter']:,} km\n"
                    f"Distance: {p['distance']:,} km\n"
                    f"Orbital Speed: {p['velocity']} km/s\n"
                    f"Angle: {p['angle']:.1f}°")
            info_label.config(text=info)
            return
    info_label.config(text="Click a planet to see info")

screen.onclick(planet_info)

# ----------------- Update Simulation -----------------
def update_simulation():
    global sun_x, last_time

    if not paused.get():
        zoom = zoom_var.get()
        speed_mult = speed_var.get()
        show_trails = show_trails_var.get()

        current_time = time.time()
        dt = current_time - last_time
        last_time = current_time

        # Move Sun forward
        sun_x += sun_speed * dt * speed_mult

        # Drift stars
        star_t.clear()
        for s in stars:
            s[0] -= 20 * dt * speed_mult
            if s[0] < -520:   # wrap around
                s[0] = 520
                s[1] = random.randint(-350, 350)
            star_t.goto(s[0], s[1])
            star_t.dot(2, "white")

        # --- Sun Tail Effect ---
        sun_trail.append((0, 0))  # Sun is at center
        if len(sun_trail) > 40:
            sun_trail.pop(0)

        sun_tail.clear()
        for i, (sx, sy) in enumerate(sun_trail):
            alpha = i / len(sun_trail)
            sun_tail.goto(sx - i * 6, sy)  # push back in X direction
            sun_tail.dot(int(12 * (1 - alpha) + 3), "orange")

        # Update planets
        for p in planets:
            p["angle"] += p["speed"] * dt * speed_mult
            angle_rad = math.radians(p["angle"])

            real_x = sun_x + math.cos(angle_rad) * p["radius"] * zoom
            real_y = math.sin(angle_rad) * p["radius"] * zoom

            screen_x = real_x - sun_x
            screen_y = real_y

            p["turtle"].goto(screen_x, screen_y)

            # Trails
            if show_trails:
                p["trail"].append((screen_x, screen_y))
                if len(p["trail"]) > 50:
                    p["trail"].pop(0)

                p["trail_t"].clear()
                for tx, ty in p["trail"]:
                    p["trail_t"].goto(tx, ty)
                    p["trail_t"].dot(2, p["turtle"].color()[0])
            else:
                p["trail"].clear()
                p["trail_t"].clear()

            # Label planet name
            p["label"].clear()
            p["label"].goto(screen_x + 8, screen_y + 8)
            p["label"].write(p["name"], font=("Arial", 7, "normal"))

            # Moon orbiting Earth
            if p["name"] == "Earth":
                moon["angle"] += moon["speed"] * dt * speed_mult
                mx = screen_x + math.cos(moon["angle"]) * moon["radius"]
                my = screen_y + math.sin(moon["angle"]) * moon["radius"]
                moon["turtle"].goto(mx, my)

            # Saturn rings
            if p["name"] == "Saturn":
                ring_t.clear()
                ring_t.penup()
                ring_t.goto(screen_x, screen_y - 12)
                ring_t.pendown()
                ring_t.circle(20)
                ring_t.penup()
                ring_t.goto(screen_x, screen_y - 18)
                ring_t.pendown()
                ring_t.circle(25)

       

    screen.update()
    root.after(30, update_simulation)

# ----------------- Start Simulation -----------------
update_simulation()
root.mainloop()
