import numpy as np
from scipy.integrate import odeint
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Определяем переменную величину
frames = 365
seconds_in_year = 365 * 24 * 60 * 60
seconds_in_day = 24 * 60 * 60
years = 0.5
t = np.linspace(0, years*seconds_in_year, frames)

def collision(x1, vx1, x2, vx2, r1, r2, m1, m2):
    """Аргументы функции:
    x1, vx1 - координата и скорость 1-ой частицы
    x2, vx2 - координата и скорость 2-ой частицы
    r1, r2, m1, m2 - радиусы и массы частиц
    """

    # Расчет расстояния между центрами частиц
    r12 = x1 - x2

    # Проверка условия на столкновение: расстояние
    # должно быть меньше суммы радиусов частиц
    if r12 <= r1 + r2:
        # Пересчет  скорости первой частицы
        VX1 = vx1 * (m1 - m2) / (m1 + m2) \
              + 2 * m2 * vx2 / (m1 + m2)

        # Пересчет скорости второй частицы
        VX2 = vx2 * (m2 - m1) / (m1 + m2) \
              + 2 * m1 * vx1 / (m1 + m2)

    else:
        # Eсли условие столкновнеия не выполнено,
        # то скорости частиц не пересчитываются
        VX1, VX2 = vx1, vx2

    return VX1, VX2

# Определяем функцию для системы диф. уравнений
def move_func(s, t):
    (x1, v_x1, y1, v_y1,
     x2, v_x2, y2, v_y2,
     x3, v_x3, y3, v_y3) = s

    # Динамика первого тела под влиянием второго и третьего
    dxdt1 = v_x1
    dv_xdt1 = (
      	    - G * m2 * (x1 - x2)
               / ((x1 - x2)**2 + (y1 - y2)**2)**1.5
            - G * m3 * (x1 - x3)
               / ((x1 - x3)**2 + (y1 - y3)**2)**1.5
              )
    dydt1 = v_y1
    dv_ydt1 = (
      	    - G * m2 * (y1 - y2)
               / ((x1 - x2)**2 + (y1 - y2)**2)**1.5
            - G * m2 * (y1 - y3)
               / ((x1 - x3)**2 + (y1 - y3)**2)**1.5
    	      )

    # Динамика второго тела под влиянием первого и третьего
    dxdt2 = v_x2
    dv_xdt2 = (
      	    - G * m1 * (x2 - x1)
               / ((x2 - x1)**2 + (y2 - y1)**2)**1.5
            - G * m3 * (x2 - x3)
               / ((x2 - x3)**2 + (y2 - y3)**2)**1.5
    	      )
    dydt2 = v_y2
    dv_ydt2 = (
      	    - G * m1 * (y2 - y1)
               / ((x2 - x1)**2 + (y2 - y1)**2)**1.5
            - G * m3 * (y2 - y3)
               / ((x2 - x3)**2 + (y2 - y3)**2)**1.5
              )

    # Динамика третьего тела под влиянием второго и первого
    dxdt3 = v_x3
    dv_xdt3 = (
      	    - G * m1 * (x3 - x1)
               / ((x3 - x1)**2 + (y3 - y1)**2)**1.5
            - G * m2 * (x3 - x2)
               / ((x3 - x2)**2 + (y3 - y2)**2)**1.5
              )
    dydt3 = v_y3
    dv_ydt3 = (
      	    - G * m1 * (y3 - y1)
               / ((x3 - x1)**2 + (y3 - y1)**2)**1.5
            - G * m2 * (y3 - y2)
               / ((x3 - x2)**2 + (y3 - y2)**2)**1.5
              )

    return (dxdt1, dv_xdt1, dydt1, dv_ydt1,
            dxdt2, dv_xdt2, dydt2, dv_ydt2,
            dxdt3, dv_xdt3, dydt3, dv_ydt3)

# Определяем начальные значения и параметры,
# входящие в систему диф. уравнений
x10 = 0
v_x10 = 0
y10 = 0
v_y10 = 0

x20 = 149 * 10**9
v_x20 = 0
y20 = 0
v_y20 = 30000

x30 = 0
v_x30 = 15000
y30 = 149 * 10**9
v_y30 = 0

m1 = 1.998 * 10**30
m2 = 5.64 * 10**24
m3 = 3.6 * 10**22

r1 = 7000000
r2 = 7000000
r3 = 7000000

G = 6.67 * 10**(-11)

# Массивы для записи итоговых координат объектов
x1 = [x10]
y1 = [y10]
x2 = [x20]
y2 = [y20]
x3 = [x30]
y3 = [y30]

# Решаем систему диф. уравнений
# Цикл для расчета столкновений
for k in range(frames - 1):
    tau = [t[k], t[k + 1]]
    s0 = (x10, v_x10, y10, v_y10,
          x20, v_x20, y20, v_y20,
          x30, v_x30, y30, v_y30)

    sol = odeint(move_func, s0, t)

    x10 = sol[1, 0]
    y10 = sol[1, 2]
    x20 = sol[1, 4]
    y20 = sol[1, 6]
    x30 = sol[1, 8]
    y30 = sol[1, 10]

    x1.append(x10)
    y1.append(y10)
    x2.append(x20)
    y2.append(y20)
    x3.append(x30)
    y3.append(y30)

    v_x10 = sol[1, 1]
    v_y10 = sol[1, 3]
    v_x20 = sol[1, 5]
    v_y20 = sol[1, 7]
    v_x30 = sol[1, 9]
    v_y30 = sol[1, 11]

    res = collision(x20, v_x20, x30, v_x30, r2, r3, m1, m2)
    v_x20 = res[0]
    v_x30 = res[1]


# Строим решение в виде графика и анимируем
fig, ax = plt.subplots()

ball_1, = plt.plot([], [], 'o', color='r', ms=15)
line_2, = plt.plot([], [], '-', color='r')
ball_2, = plt.plot([], [], 'o', color='r', ms=5)
ball_3, = plt.plot([], [], 'o', color='r', ms=5)

def animate(i):
    ball_1.set_data((x1[i], y1[i]))
    line_2.set_data((x2[:i], y2[:i]))
    ball_2.set_data((x2[i], y2[i]))
    ball_3.set_data((x3[i], y3[i]))

plt.axis('equal')
edge = 2 * 149 * 10**9
ax.set_xlim(-edge, edge)
ax.set_ylim(-edge, edge)

ani = FuncAnimation(fig, animate, frames=frames, interval=30)
ani.save('collision.gif')