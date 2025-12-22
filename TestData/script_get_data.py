from controller import Robot
import matplotlib.pyplot as plt
import numpy as np

robot = Robot()
timestep = int(robot.getBasicTimeStep())
lidar = robot.getDevice('lidar')
lidar.enable(timestep)

MAX_RANGE = 5
SAVE_FILENAME = 'lidar_scan.npy'
is_saved = False
save_delay = 2.0

plt.ion()
fig, ax = plt.subplots()
ax.set_xlim(-MAX_RANGE, MAX_RANGE)
ax.set_ylim(-MAX_RANGE, MAX_RANGE)
ax.set_aspect('equal')
scat = ax.scatter([], [], s=2, c='red')

while robot.step(timestep) != -1:
    ranges = np.array(lidar.getRangeImage())
    fov = lidar.getFov()
    width = lidar.getHorizontalResolution()
    angles = np.linspace(fov / 2, -fov / 2, width)

    mask = (ranges < lidar.getMaxRange()) & (ranges > lidar.getMinRange())

    r_valid = ranges[mask]
    a_valid = angles[mask]

    x = r_valid * np.cos(a_valid)
    y = r_valid * np.sin(a_valid)

    data = np.stack([x, y], axis=1)

    if data.size > 0:
        scat.set_offsets(data)

    if not is_saved and robot.getTime() > save_delay:
        np.save(SAVE_FILENAME, data)
        print(f"Points saved: {len(data)}")
        is_saved = True
    plt.pause(0.01)
