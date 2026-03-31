import numpy as np
import matplotlib.pyplot as plt

x_max = 17
alpha = -2
y_min = 0
y_max = 255
arrow_number_per_period = 6
linear_flag = True
A = 30
length = 36
m_y = -25

def exponential_sawtooth(phase, alpha):
    return (np.exp(alpha * phase) - 1) / (np.exp(alpha) - 1)

def get_arrow_start_end(m_x, m_y, A, gs, px_per_x_unit, px_per_y_unit):
    phi = np.radians(gs * (180/255)) + np.pi/2
    a_vector = A/2 * np.array([np.cos(phi) * (1/px_per_x_unit), np.sin(phi) * (1/px_per_y_unit)])
    m_vector = np.array([m_x, m_y])
    x = m_vector - a_vector
    y = m_vector + a_vector

    return (x[0], x[1]), (y[0], y[1])

if linear_flag:
    sawtooth = lambda: phase
else:
    sawtooth = lambda: exponential_sawtooth(phase, alpha)

x = np.arange(length)
phase = (x % x_max) / (x_max - 1)
values = y_min + sawtooth() * (y_max - y_min)

fig, ax = plt.subplots(figsize=(6, 4), dpi=100)  # 6x4 inch, 100 dpi → 600x400 Pixel

ax.plot(values)
ax.set_title('Sawtooth')
ax.set_xlabel('Width [px]')
ax.set_ylabel('gray value')
ax.set_ylim(-50, 260)

fig.canvas.draw()
trans = ax.transData

origin = trans.transform((0, 0))
x_unit = trans.transform((1, 0))
y_unit = trans.transform((0, 1))

px_per_x_unit = x_unit[0] - origin[0]
px_per_y_unit = y_unit[1] - origin[1]


arrow_number = int((length / x_max)*arrow_number_per_period)

value_index = np.linspace(0, len(values) -1, arrow_number)
for i, m_x in enumerate(np.linspace(0, length-1, arrow_number)):
    gs = values[int(value_index[i])]
    x, y = get_arrow_start_end(m_x, m_y, A, gs, px_per_x_unit, px_per_y_unit)
    ax.annotate(
        '',
        xy=y,  # Ende
        xytext=x,  # Start
        arrowprops=dict(arrowstyle='<->', color='red')
    )
fig.tight_layout()
plt.show()