import numpy as np
import matplotlib.pyplot as plt
from PIL.GimpGradientFile import linear

x_max = 17
alpha = -5
y_min = 0
y_max = 255
arrow_number = 25
linear_flag = True
A = 0.05

def exponential_sawtooth(phase, alpha):
    return (np.exp(alpha * phase) - 1) / (np.exp(alpha) - 1)

def get_arrow_start_end(m_x, m_y, A, gs):
    phi = np.radians(gs * (180/255))
    a_vector = A/2 * np.array([np.cos(phi), np.sin(phi)])
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

fig, (ax_sawtooth, ax_arrow) = plt.subplots(2, gridspec_kw={'height_ratios': [1, 1]})

ax_sawtooth.plot(values)
ax_sawtooth.set_title('Sawtooth')
ax_sawtooth.set_xlabel('Width [px]')
ax_sawtooth.set_ylabel('gray value')
ax_arrow.set_title('Polarisation Pattern')
ax_arrow.set_ylim(0, 0.35)
ax_arrow.axis('off')


m_y = 0.175
value_index = np.linspace(0, len(values) -1, arrow_number)
for i, m_x in enumerate(np.linspace(0, 1, arrow_number)):
    gs = values[int(value_index[i])]
    x, y = get_arrow_start_end(m_x, m_y, A, gs)
    ax_arrow.annotate(
        '',
        xy=y,  # Ende
        xytext=x,  # Start
        arrowprops=dict(arrowstyle='->', color='red')
    )
fig.tight_layout()
plt.show()