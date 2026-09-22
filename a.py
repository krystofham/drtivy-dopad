import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

from Space import Space
from SystemState import SystemState
from RK4Stepper import RK4Stepper

AU = 1.496e11

# "sun"   -> Slunce stojí v (0,0,0), Země i meteor se pohybují
# "earth" -> Země stojí v (0,0,0), Slunce obíhá a meteor se pohybuje vůči Zemi
FRAME = "sun"

DT = 5 * 60  # krok simulace [s]
T_MAX = 365 * 24 * 3600  # délka simulace [s]
STEPS_PER_FRAME = 300  # kolik RK4 kroků na jeden snímek (rychlost animace)
Z_VELOCITY = 758  # z-ová složka rychlosti meteoru
# Z_VELOCITY = 900


def starting_state(zcoord):
    return SystemState(
        EarthPosition=[
            -3.1617821569319294e10,
            1.436603570949401e11,
            117565.96043321176,
        ],
        EarthVelocity=[-29581.545053209236, -6515.282025813395, -0.010617114855559093],
        AsteroidPosition=[-1.59458654e11, -1.94077604e11, 6.61733278e09],
        AsteroidVelocity=[13224.513110762178, -14246.151046842608, zcoord],
    )


space = Space()
stepper = RK4Stepper()
state = starting_state(Z_VELOCITY)
t = 0.0
hit = False


def to_frame(st):
    """Vrátí (slunce, země, asteroid) v jednotkách AU podle zvolené soustavy."""
    sun = np.zeros(3)
    earth = st.EarthPosition.copy()
    ast = st.AsteroidPosition.copy()
    if FRAME == "earth":
        sun = sun - earth
        ast = ast - earth
        earth = np.zeros(3)
    return sun / AU, earth / AU, ast / AU


# historie pro stopy
sun0, earth0, ast0 = to_frame(state)
earth_trail = [earth0.copy()]
ast_trail = [ast0.copy()]
sun_trail = [sun0.copy()]

# ---------- vykreslení ----------
fig = plt.figure(figsize=(9, 8))
ax = fig.add_subplot(111, projection="3d")
lim = 3.0
ax.set_xlim(-lim, lim)
ax.set_ylim(-lim, lim)
ax.set_zlim(-lim * 0.3, lim * 0.3)
ax.set_box_aspect((1, 1, 0.3))
ax.set_xlabel("x [AU]")
ax.set_ylabel("y [AU]")
ax.set_zlabel("z [AU]")

(sun_dot,) = ax.plot([], [], [], "o", color="gold", markersize=14, label="Slunce")
(earth_dot,) = ax.plot([], [], [], "o", color="royalblue", markersize=7, label="Země")
(ast_dot,) = ax.plot([], [], [], "o", color="red", markersize=5, label="Asteroid")
(earth_line,) = ax.plot([], [], [], "-", color="royalblue", alpha=0.5, lw=1)
(ast_line,) = ax.plot([], [], [], "-", color="red", lw=1.5)
(sun_line,) = ax.plot([], [], [], "-", color="gold", alpha=0.5, lw=1)
title = ax.set_title("")
ax.legend(loc="upper right")


def set3d(artist, xyz):
    artist.set_data_3d(xyz[0], xyz[1], xyz[2])


def update(_frame):
    global state, t, hit
    if hit or t >= T_MAX:
        return ()

    for _ in range(STEPS_PER_FRAME):
        new_state = stepper.nextStep(t, DT, state, space)
        if space.shouldHalt(t, t + DT, state, new_state):
            hit = True
        state = new_state
        t += DT

        sun, earth, ast = to_frame(state)
        sun_trail.append(sun)
        earth_trail.append(earth)
        ast_trail.append(ast)

        if hit or t >= T_MAX:
            break

    et = np.array(earth_trail).T
    at = np.array(ast_trail).T
    st = np.array(sun_trail).T
    set3d(earth_line, et)
    set3d(ast_line, at)
    set3d(sun_line, st)
    set3d(sun_dot, st[:, -1:])
    set3d(earth_dot, et[:, -1:])
    set3d(ast_dot, at[:, -1:])

    dist = (
        np.linalg.norm(state.AsteroidPosition - state.EarthPosition) / space.EarthRadius
    )
    msg = f"den {t / 86400:.0f}   vzdálenost asteroid–Země: {dist:.0f} Poloměrů Země"
    if hit:
        ast_dot.set_label("Meteorit")
        ax.legend()
        msg += "\n**Zásah**"
    title.set_text(msg)
    return ()


anim = FuncAnimation(fig, update, interval=30, blit=False, cache_frame_data=False)
SAVE = False  # "mp4", "gif" nebo None (jen zobrazit)

if SAVE == "mp4":
    anim.save("meteor.mp4", writer="ffmpeg", fps=30, dpi=150)
plt.show()
