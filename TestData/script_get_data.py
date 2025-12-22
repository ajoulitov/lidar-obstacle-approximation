from controller import Robot
import math
import numpy as np

SAVE_PATH = "lidar_scan.npy"

SELF_COLLISION_DIST = 0.0
ROTATION_SPEED = 200.0
ROTATION_TIME_SEC = 0.5
SCAN_STEP = 20


def main():
    robot = Robot()
    timestep = int(robot.getBasicTimeStep())

    lidar = robot.getDevice("lidar")
    lidar.enablePointCloud()
    lidar.enable(timestep)
    max_range = lidar.getMaxRange()

    left_motor = robot.getDevice("left wheel motor")
    right_motor = robot.getDevice("right wheel motor")

    left_motor.setPosition(float("inf"))
    right_motor.setPosition(float("inf"))

    left_motor.setVelocity(ROTATION_SPEED)
    right_motor.setVelocity(-ROTATION_SPEED)

    all_points = []

    steps_to_rotate = int((ROTATION_TIME_SEC * 1000) / timestep)

    for step in range(steps_to_rotate):
        if robot.step(timestep) == -1:
            break

        if step % SCAN_STEP != 0:
            continue

        point_cloud = lidar.getPointCloud()
        if not point_cloud:
            continue

        for point in point_cloud:
            distance = math.sqrt(
                point.x * point.x + point.y * point.y + point.z * point.z
            )
            if SELF_COLLISION_DIST < distance <= max_range:
                all_points.append([point.x, point.y])

    left_motor.setVelocity(0.0)
    right_motor.setVelocity(0.0)

    points = np.array(all_points, dtype=float)
    np.save(SAVE_PATH, points)

    while robot.step(timestep) != -1:
        pass


if __name__ == "__main__":
    main()
