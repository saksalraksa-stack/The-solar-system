import turtle as T
import math
import random

# --- Setup screen ---
screen = T.Screen()
screen.bgcolor("black")
screen.title("Solar System Simulation")
screen.tracer(False)  # Manual update for smooth animation

# --- Draw stars (background space) ---
def draw_stars(n=3000):
    star = T.Turtle(visible=False)
    star.hideturtle()
    star.speed(0)
    star.color("white")
    star.penup()
    for _ in range(n):
        x = random.randint(-800, 800)
        y = random.randint(-500, 500)
        star.goto(x, y)
        size = random.choice([1, 2, 3])
        star.dot(size)

draw_stars()

# --- Draw Small Sun with Glow ---
def draw_sun():
    sun = T.Turtle(visible=False)
    sun.hideturtle()
    sun.speed(0)

    # Small glow layers (soft effect)
    for r in range(35, 20, -3):  # glow outside the core
        sun.penup()
        sun.goto(0, -r)
        sun.pendown()
        sun.color("gold")
        sun.begin_fill()
        sun.circle(r)
        sun.end_fill()

    # Core of the Sun
    core_radius = 18
    sun.penup()
    sun.goto(0, -core_radius)
    sun.pendown()
    sun.color("yellow")
    sun.begin_fill()
    sun.circle(core_radius)
    sun.end_fill()

draw_sun()  # ✅ Call it so the sun actually shows up

# --- Function to draw ellipse ---
def draw_ellipse(a, b, color="white"):
    t = T.Turtle(visible=False)
    t.hideturtle()
    t.speed(0)
    t.color(color)
    t.penup()
    points = []
    for angle in range(360):
        x = a * math.cos(math.radians(angle))
        y = b * math.sin(math.radians(angle))
        points.append((x, y))
    t.goto(points[0])
    t.pendown()
    for x, y in points:
        t.goto(x, y)

# --- Draw all orbits ---
def draw_all_orbits():
    orbits = [
        (120, 75),   # Mercury
        (180, 120),  # Venus
        (240, 165),  # Earth
        (300, 210),  # Mars
        (375, 255),  # Jupiter
        (450, 315),  # Saturn
        (525, 375),  # Uranus
        (615, 435)   # Neptune
    ]
    for a, b in orbits:
        draw_ellipse(a, b, color="white")

draw_all_orbits()

# --- Planet class ---
class Planet:
    def __init__(self, name, color, a, b, size, speed, diameter_km,
                 density_g_cm3, mass_kg, distance_million_km):
        self.name = name
        self.color = color
        self.a = a  # semi-major axis
        self.b = b  # semi-minor axis
        self.size = size
        self.speed = speed
        self.angle = 0

        # Physical properties
        self.diameter_km = diameter_km
        self.mass_kg = mass_kg
        self.density = density_g_cm3
        self.distance_million_km = distance_million_km

        # Create turtle for planet
        self.t = T.Turtle()
        self.t.shape("circle")
        self.t.color(color)
        self.t.shapesize(stretch_wid=size, stretch_len=size)
        self.t.penup()

        # Label turtle for planet info
        self.label = T.Turtle(visible=False)
        self.label.hideturtle()
        self.label.color("white")
        self.label.penup()

    def move(self):
        # Update angle
        self.angle = (self.angle + self.speed) % 360
        rad = math.radians(self.angle)
        x = self.a * math.cos(rad)
        y = self.b * math.sin(rad)
        self.t.goto(x, y)

        # Clear previous info and write new
        self.label.clear()
        info_text = f"{self.name}\n" \
                    f"Diameter: {self.diameter_km} km\n" \
                    f"Mass: {self.mass_kg:.2e} kg\n" \
                    f"Density: {self.density} g/cm³\n" \
                    f"Dist from Earth: {self.distance_million_km}M km\n" \
                    f"Speed: {self.speed:.2f}°/step"
        self.label.goto(x, y + 15)  # Display above planet
        self.label.write(info_text, align="center",
                         font=("Arial", 10, "normal"))

# --- Create planets ---
planets = [
    Planet("Mercury", "gray", 120, 75, 0.4, 4.7*2, 4880, 5.43, 3.3e23, 91),
    Planet("Venus", "orange", 180, 120, 0.6, 3.5*2, 12104, 5.24, 4.87e24, 41),
    Planet("Earth", "blue", 240, 165, 0.7, 3.0*2, 12742, 5.52, 5.97e24, 0),
    Planet("Mars", "red", 300, 210, 0.5, 2.4*2, 6779, 3.93, 0.642e24, 78),
    Planet("Jupiter", "brown", 375, 255, 1.5, 1.3*2, 139820, 1.33, 1898e24, 628),
    Planet("Saturn", "gold", 450, 315, 1.2, 1.0*2, 116460, 0.69, 568e24, 1275),
    Planet("Uranus", "lightblue", 525, 375, 1.0, 0.7*2, 50724, 1.27, 86.8e24, 2720),
    Planet("Neptune", "purple", 615, 435, 1.0, 0.5*2, 49244, 1.64, 102e24, 4350)
]

# --- Instructions in a box ---
instr_turtle = T.Turtle(visible=False)
instr_turtle.hideturtle()
instr_turtle.penup()
instr_turtle.color("white")
show_instr = True  # Start by showing instructions

def show_instructions():
    instr_turtle.clear()
    if show_instr:
        # Draw box
        x_left, y_top = -300, -100
        width, height = 620, 150
        instr_turtle.goto(x_left, y_top)
        instr_turtle.pendown()
        instr_turtle.pensize(10)
        instr_turtle.fillcolor("gray")
        instr_turtle.begin_fill()
        
        for _ in range(2):
            instr_turtle.forward(width)
            instr_turtle.right(90)
            instr_turtle.forward(height)
            instr_turtle.right(90)
        instr_turtle.end_fill()
        instr_turtle.penup()

        # Write instructions inside box
        instr_turtle.goto(0, -250)
        instructions_text = (
            "                                  Instruction Controls:\n"
            "(+)  Click SPACE: Pause / Resume\n"
            "(+)  Click ' i ' : show or not show instruction\n"
            "(+)  Click UP Arrow or '+': Increase speed of all planets\n"
            "(+)  Click DOWN Arrow or '-': Decrease speed of all planets\n" 
        )
        instr_turtle.write(instructions_text, align="center", font=("Arial", 16, "bold"))

def toggle_instructions():
    global show_instr
    show_instr = not show_instr
    show_instructions()

# --- Animation loop with pause/resume ---
paused = False  # global flag
def toggle_pause():
    global paused
    paused = not paused
    if paused:
        print("Paused")
    else:
        print("Resumed")

# --- Functions to adjust ALL planets ---
def speed_up_all():
    for p in planets:
        p.speed *= 1.2
    print("All planets sped up")
def slow_down_all():
    for p in planets:
        p.speed *= 0.8
    print("All planets slowed down")

# --- Key bindings ---
screen.listen()
screen.onkey(toggle_pause, "space")
screen.onkey(toggle_instructions, "i")   # Press 'i' to show/hide instructions
screen.onkey(speed_up_all, "Up")   # Press ↑ arrow
screen.onkey(speed_up_all, "+")    # Press + key
screen.onkey(slow_down_all, "Down") # Press ↓ arrow
screen.onkey(slow_down_all, "-")    # Press - key

def animate():
    for planet in planets:
        if not paused:
            planet.move()
    screen.update()
    screen.ontimer(animate, 30)  # ~33 FPS

animate()
screen.mainloop()
