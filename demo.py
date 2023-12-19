import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider, Button


def pc_func(x: np.array, C, L1, L2, D) -> np.array:
    return C * np.sin(2 * x) + L1 * np.sin(4 * x) + L2 * np.cos(4 * x) + D


x = np.linspace(0, np.pi, 100)
C, L1, L2, D = 0, 0, 0, 0

fig, ax = plt.subplots()
plt.title("Photocurrents in Bi2Se3 Demo")
line, = ax.plot(x, pc_func(x, C, L1, L2, D))
ax.set_xlabel("Polarization [rad]")
ax.set_ylabel("Current [arb. units]")
fig.subplots_adjust(bottom=0.3)

# Vertical Lines
ax.axvline(x=0, color='g', linestyle=':', linewidth=2)
ax.axvline(x=np.pi/2, color='g', linestyle=':', linewidth=2)
ax.axvline(x=np.pi, color='g', linestyle=':', linewidth=2)
ax.axvline(x=np.pi/4, color='b', linestyle=':', linewidth=2)
ax.axvline(x=3*np.pi/4, color='r', linestyle=':', linewidth=2)

# Sliders
axC = fig.add_axes([0.05, 0.1, 0.35, 0.1])
sliderC = Slider(ax=axC, label="C", valmin=-5, valmax=5, valinit=C)
axL1 = fig.add_axes([0.55, 0.1, 0.35, 0.1])
sliderL1 = Slider(ax=axL1, label="L1", valmin=-5, valmax=5, valinit=L1)
axL2 = fig.add_axes([0.05, 0, 0.35, 0.1])
sliderL2 = Slider(ax=axL2, label="L2", valmin=-5, valmax=5, valinit=L2)
axD = fig.add_axes([0.55, 0, 0.35, 0.1])
sliderD = Slider(ax=axD, label="D", valmin=-5/0.07, valmax=5/0.07, valinit=D)

def update(val):
    C, L1, L2, D = sliderC.val, sliderL1.val, sliderL2.val, sliderD.val
    line.set_ydata(pc_func(x, C, L1, L2, D))
    abslim = abs(C) + abs(L1) + abs(L2)
    plt.axes(ax)
    plt.ylim(D - abslim*1.15, D + abslim*1.15)
    fig.canvas.draw_idle()

sliderC.on_changed(update)
sliderL1.on_changed(update)
sliderL2.on_changed(update)
sliderD.on_changed(update)

plt.show()