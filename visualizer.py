import numpy as np
import matplotlib.pyplot as plt
from PIL.GimpGradientFile import linear

x_max = 17
alpha = -5
y_min = 0
y_max = 255
arrow_number = 15
linear_flag = True
A = 1.5
A_px = 20

def exponential_sawtooth(phase, alpha):
    return (np.exp(alpha * phase) - 1) / (np.exp(alpha) - 1)

def get_arrow_start_end(m_x, m_y, A, gs, a_y_scale):
    phi = np.radians(gs * (180/255))
    a_vector = A/2 * np.array([np.cos(phi), (np.sin(phi)*a_y_scale)])
    m_vector = np.array([m_x, m_y])
    x = m_vector - a_vector
    y = m_vector + a_vector

    return (x[0], x[1]), (y[0], y[1])

if linear_flag:
    sawtooth = lambda: x
else:
    sawtooth = lambda: exponential_sawtooth(x, alpha)

x = np.linspace(0, 1, x_max)
values = y_min + sawtooth() * (y_max - y_min)

fig, ax = plt.subplots(figsize=(6, 4), dpi=100)  # 6x4 inch, 100 dpi → 600x400 Pixel

ax.plot(values)
ax.set_title('Sawtooth')
ax.set_xlabel('Width [px]')
ax.set_ylabel('gray value')
ax.set_ylim(-50, 260)

# Transformationsmatrix von Daten -> Figure
bbox = ax.get_window_extent().transformed(fig.dpi_scale_trans.inverted())
width_inch, height_inch = bbox.width, bbox.height

# Datenbereich
x_range = ax.get_xlim()[1] - ax.get_xlim()[0]
y_range = ax.get_ylim()[1] - ax.get_ylim()[0]

# Pixel pro Daten-Einheit
dpi = fig.dpi
px_per_data_x = (width_inch * dpi) / x_range
px_per_data_y = (height_inch * dpi) / y_range

a_y_scale = A_px / px_per_data_y

m_y = 0
value_index = np.linspace(0, len(values) -1, arrow_number)
for i, m_x in enumerate(np.linspace(0, x_max, arrow_number)):
    gs = values[int(value_index[i])]
    x, y = get_arrow_start_end(m_x, m_y, A, gs, a_y_scale)
    ax.annotate(
        '',
        xy=y,  # Ende
        xytext=x,  # Start
        arrowprops=dict(arrowstyle='->', color='red')
    )
fig.tight_layout()
plt.show()