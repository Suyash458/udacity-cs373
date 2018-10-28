import random
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.axes3d import Axes3D, get_test_data
from matplotlib import cm
from copy import copy
from utils import Robot

def make_robot():
    robot = Robot()
    robot.set(0.0, 1.0, 0.0)
    robot.set_steering_drift(10.0 / 180.0 * np.pi)
    return robot

def run(robot, params, n=100, speed=1.0):
    x_trajectory = []
    y_trajectory = []
    err = 0
    prev_cte = robot.y
    int_cte = 0
    for i in range(2 * n):
        cte = robot.y
        diff_cte = cte - prev_cte
        int_cte += cte
        prev_cte = cte
        steer = -params[0] * cte - params[1] * diff_cte - params[2] * int_cte
        robot.move(steer, speed)
        x_trajectory.append(robot.x)
        y_trajectory.append(robot.y)
        if i >= n:
            err += cte ** 2
    return x_trajectory, y_trajectory, err / n

def twiddle(tol=0.05): 
    p = [0.0, 0.0, 0.0]
    dp = [1.0, 1.0, 1.0]
    robot = make_robot()
    x_trajectory, y_trajectory, best_err = run(robot, p)
    while sum(dp) > tol:
        for i in range(len(p)):
            p[i] += dp[i]
            robot = make_robot()
            _, _, err = run(robot, p)   
            if err < best_err:
                dp[i] *= 1.1
                best_err = err
            else:
                p[i] -= 2*dp[i]
                robot = make_robot()                
                _, _, err = run(robot, p)
                if err < best_err:
                    dp[i] *= 1.1
                    best_err = err                    
                else:
                    p[i] += dp[i]
                    dp[i] *= 0.9
        yield copy(p), best_err
    yield copy(p), best_err

fig = plt.figure()
ax2 = fig.add_subplot(1, 1, 1, projection='3d')
X = np.random.uniform(-2, 15, 10000)
Y = np.random.uniform(0, 20, 10000)
Z = np.random.uniform(-1.5, 1.5, 10000)
params = np.column_stack((X, Y, Z))
c = []
twiddle_path = []

for (p, err) in twiddle():
    twiddle_path.append(p)

twiddle_path = np.array(twiddle_path)

for i in params:
    robot = make_robot()
    x_trajectory, y_trajectory, err = run(robot, i)  
    if err <= 0.1:
        c.append(10)
    elif 0.1 < err <= 10:
        c.append(30)
    elif 10 < err <= 100:
        c.append(40)    
    elif 100 < err <= 500:
        c.append(50)        
    elif 500 < err <= 1000:
        c.append(60)        
    elif 1000 < err <= 1500:
        c.append(70)
    elif 1500 < err <= 2000:
        c.append(80)
    elif 2000 < err:
        c.append(90)
C = np.array(c)

plt.plot(twiddle_path[:, 0], twiddle_path[:, 1], twiddle_path[:,2], linewidth=8)

ax2.scatter(X, Y, Z, c=C, s=60, cmap='Reds_r', alpha=0.1)
plt.show()
