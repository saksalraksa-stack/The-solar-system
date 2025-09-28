
"""
Solar System with Python Turtle
--------------------------------
- Sun at center
- 4 planets with different sizes, colors, and orbits (one elliptical)
- Motion with an animation loop (ontimer)
- Labels for each planet
- Optional enhancements:
    * Stars background
    * Earth has one moon
    * Keyboard controls for speed, pause, trails, and showing orbits
Controls:
  [Space] Pause/Resume animation
  [+]     Speed up
  [-]     Slow down
  [T]     Toggle planet trails
  [O]     Toggle orbit guides on/off
  [Q]     Quit
"""
import math
import random
import turtle as T

# ---------- Screen setup ----------
WIDTH, HEIGHT = 1000, 700
screen = T.Screen()
screen.setup(WIDTH, HEIGHT)
screen.bgcolor("black")
screen.title("Python Turtle — Mini Solar System")
screen.tracer(False)  # We will manually update frames

# ---------- Utility ----------
def draw_stars(n=120):
    rng = random.Random(42)  # deterministic
    star = T.Turtle(visible=False)
    star.hideturtle()
    star.speed(0)
    star.color("white")
    star.penup()
    for _ in range(n):
        x = rng.randint(-WIDTH//2 + 10, WIDTH//2 - 10)
        y = rng.randint(-HEIGHT//2 + 10, HEIGHT//2 - 10)
        star.goto(x, y)
        size = rng.choice([1,1,2,2,3])
        star.dot(size)

def deg2rad(d): 
    return d * math.pi / 180.0

def rotated(x, y, tilt_deg):
    t = deg2rad(tilt_deg)
    ct, st = math.cos(t), math.sin(t)
    return x*ct - y*st, x*st + y*ct

# Draw the Sun with a simple "glow"
def draw_sun():
    sun = T.Turtle(visible=False)
    sun.hideturtle()
    sun.speed(0)
    sun.penup()
    sun.goto(0, -20)
    sun.color("#FDB813")
    sun.pendown()
    sun.begin_fill()
    sun.circle(20)
    sun.end_fill()
    # glow rings
    sun.penup()
    for r, alpha in [(40, 0.35), (70, 0.18), (100, 0.10)]:
        sun.goto(0, -r)
        sun.pendown()
        sun.pensize(2)
        sun.color(1.0, 0.72, 0.07, )
        sun.circle(r)
        sun.penup()
    return sun

# ---------- Orbits ----------
def draw_orbit_ellipse(a, b=None, tilt=0, color="#333333"):
    """Return a Turtle that draws (and keeps) the orbit guide."""
    if b is None: b = a
    orb = T.Turtle(visible=False)
    orb.hideturtle()
    orb.speed(0)
    orb.pensize(1)
    orb.color(color)
    orb.penup()
    steps = 360
    # move to start point
    x0, y0 = rotated(a, 0, tilt)
    orb.goto(x0, y0)
    orb.pendown()
    for d in range(1, steps+1):
        t = deg2rad(d)
        x, y = a*math.cos(t), b*math.sin(t)
        x, y = rotated(x, y, tilt)
        orb.goto(x, y)
    orb.penup()
    return orb

# ---------- Planet classes ----------
class Planet:
    def __init__(self, name, color, size_px, orbit_a, orbit_b=None, speed_deg=1.0, tilt=0, start_angle=0, show_orbit=True):
        self.name = name
        self.color = color
        self.size_px = size_px
        self.a = orbit_a
        self.b = orbit_b if orbit_b is not None else orbit_a
        self.tilt = tilt  # degrees
        self.base_speed = speed_deg
        self.theta = start_angle  # current angle in degrees
        self.trail = False
        # body turtle
        self.t = T.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.t.shape("circle")
        self.t.color(color)
        scale = max(self.size_px / 20.0, 0.2)  # 20px default circle
        self.t.shapesize(scale, scale)
        self.t.penup()
        # label turtle
        self.label = T.Turtle(visible=False)
        self.label.hideturtle()
        self.label.speed(0)
        self.label.color("white")
        self.label.penup()
        # orbit guide
        self.orbit_drawer = draw_orbit_ellipse(self.a, self.b, self.tilt) if show_orbit else None
        self.visible = True
        self._pos = (0.0, 0.0)

    def position(self):
        """Return current x, y coordinates (and store)."""
        th = deg2rad(self.theta)
        x, y = self.a*math.cos(th), self.b*math.sin(th)
        x, y = rotated(x, y, self.tilt)
        self._pos = (x, y)
        return x, y

    def move(self, speed_scale=1.0):
        self.theta = (self.theta + self.base_speed * speed_scale) % 360.0
        x, y = self.position()
        if self.trail:
            self.t.pendown()
        else:
            self.t.penup()
        self.t.goto(x, y)
        if not self.t.isvisible():
            self.t.showturtle()
        # label slightly offset
        self.label.clear()
        self.label.goto(x + 8, y + 10)
        self.label.write(self.name, align="left", font=("Arial", 10, "normal"))

    def toggle_orbit(self, show: bool):
        if show and self.orbit_drawer is None:
            self.orbit_drawer = draw_orbit_ellipse(self.a, self.b, self.tilt)
        elif not show and self.orbit_drawer is not None:
            self.orbit_drawer.clear()
            self.orbit_drawer.hideturtle()
            self.orbit_drawer = None

    @property
    def x(self): return self._pos[0]
    @property
    def y(self): return self._pos[1]


class Moon:
    def __init__(self, name, color, size_px, parent: Planet, orbit_r=25, speed_deg=6.0, start_angle=0):
        self.name = name
        self.color = color
        self.size_px = size_px
        self.parent = parent
        self.r = orbit_r
        self.base_speed = speed_deg
        self.theta = start_angle
        self.trail = False
        # body
        self.t = T.Turtle()
        self.t.hideturtle()
        self.t.speed(0)
        self.t.shape("circle")
        self.t.color(color)
        scale = max(self.size_px / 20.0, 0.2)
        self.t.shapesize(scale, scale)
        self.t.penup()
        # label
        self.label = T.Turtle(visible=False)
        self.label.hideturtle()
        self.label.speed(0)
        self.label.color("white")
        self.label.penup()
        # orbit guide (relative to parent, drawn dynamically is messy; omit fixed guide)
        self.orbit_drawer = None

    def move(self, speed_scale=1.0):
        self.theta = (self.theta + self.base_speed * speed_scale) % 360.0
        th = deg2rad(self.theta)
        px, py = self.parent.x, self.parent.y
        x, y = px + self.r*math.cos(th), py + self.r*math.sin(th)
        if self.trail:
            self.t.pendown()
        else:
            self.t.penup()
        self.t.goto(x, y)
        if not self.t.isvisible():
            self.t.showturtle()
        self.label.clear()
        self.label.goto(x + 6, y + 8)
        self.label.write(self.name, align="left", font=("Arial", 9, "normal"))

    def toggle_orbit(self, show: bool):
        # For simplicity, re-draw relative orbit each time when show=True.
        if not show:
            if self.orbit_drawer:
                self.orbit_drawer.clear()
                self.orbit_drawer.hideturtle()
                self.orbit_drawer = None
        else:
            if self.orbit_drawer is None:
                self.orbit_drawer = T.Turtle(visible=False)
                self.orbit_drawer.hideturtle()
                self.orbit_drawer.speed(0)
                self.orbit_drawer.color("#333333")
            # Draw a small circle around current parent position
            self.orbit_drawer.clear()
            self.orbit_drawer.penup()
            self.orbit_drawer.goto(self.parent.x, self.parent.y - self.r)
            self.orbit_drawer.pendown()
            self.orbit_drawer.circle(self.r)
            self.orbit_drawer.penup()


# ---------- Build the scene ----------
draw_stars(160)
sun = draw_sun()

planets = []
# name, color, size_px, a, b, speed, tilt
planets.append(Planet("Mercury", "#A3A3A3", 8, orbit_a=70, orbit_b=60, speed_deg=3.6, tilt=10))
planets.append(Planet("Venus",   "#E39F3A", 12, orbit_a=110, orbit_b=105, speed_deg=1.8, tilt=-5))
earth = Planet("Earth",   "#1E90FF", 12, orbit_a=150, orbit_b=150, speed_deg=1.2, tilt=0)
planets.append(earth)
planets.append(Planet("Mars",    "#D14B3D", 10, orbit_a=190, orbit_b=180, speed_deg=0.96, tilt=15))

moons = []
moons.append(Moon("Moon", "#C0C0C0", 6, parent=earth, orbit_r=24, speed_deg=5.0))

# ---------- Controls & Animation ----------
state = {
    "paused": False,
    "trail": False,
    "show_orbits": True,
    "speed_scale": 1.0,
}

def toggle_pause():
    state["paused"] = not state["paused"]

def speed_up():
    state["speed_scale"] *= 1.25

def slow_down():
    state["speed_scale"] /= 1.25

def toggle_trails():
    state["trail"] = not state["trail"]
    for p in planets: p.trail = state["trail"]
    for m in moons: m.trail = state["trail"]

def toggle_orbits():
    state["show_orbits"] = not state["show_orbits"]
    for p in planets: p.toggle_orbit(state["show_orbits"])
    for m in moons: m.toggle_orbit(state["show_orbits"])

def quit_app():
    try:
        screen.bye()
    except T.Terminator:
        pass

# On-screen help
help_t = T.Turtle(visible=False)
help_t.hideturtle()
help_t.color("white")
help_t.penup()
help_lines = [
    "[Space] Pause/Resume  [+/-] Speed  [T] Trails  [O] Toggle orbits  [Q] Quit"
]
help_t.goto(-WIDTH//2 + 14, HEIGHT//2 - 24)
help_t.write(help_lines[0], align="left", font=("Arial", 12, "normal"))

screen.listen()
screen.onkey(toggle_pause, "space")
screen.onkey(speed_up, "+")
screen.onkey(speed_up, "=")  # convenience
screen.onkey(slow_down, "-")
screen.onkey(toggle_trails, "t")
screen.onkey(toggle_orbits, "o")
screen.onkey(quit_app, "q")

def animate():
    if not state["paused"]:
        for p in planets:
            p.move(speed_scale=state["speed_scale"])
        for m in moons:
            # keep moon orbit guide around current parent if visible
            if state["show_orbits"]:
                m.toggle_orbit(True)
            m.move(speed_scale=state["speed_scale"])
    screen.update()
    screen.ontimer(animate, 20)  # ~50 FPS

animate()

# Keep window open
screen.mainloop()
