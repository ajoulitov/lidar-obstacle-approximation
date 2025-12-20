from controller import Robot
import numpy as np

SAVE_PATH = "lidar_scan.npy"
SELF_COLLISION_DIST = 0.2


class LidarSingleSaver:
    def __init__(self, robot: Robot, save_path: str = SAVE_PATH, self_collision_dist: float = SELF_COLLISION_DIST):
        self.robot = robot
        self.timestep = int(self.robot.getBasicTimeStep())
        self.lidar = self.robot.getDevice("lidar")
        self.lidar.enablePointCloud()
        self.lidar.enable(self.timestep)
        self.save_path = save_path
        self.self_collision_dist = float(self_collision_dist)

    def _get_points_2d(self):
        pc = self.lidar.getPointCloud()
        if not pc:
            return []
        max_r = self.lidar.getMaxRange()
        pts = []
        for p in pc:
            d = (p.x * p.x + p.y * p.y + p.z * p.z) ** 0.5
            if self.self_collision_dist < d <= max_r:
                pts.append([float(p.x), float(p.y)])
        return pts

    def run_once_and_save(self):
        self.robot.step(self.timestep)
        points = self._get_points_2d()
        np.save(self.save_path, np.array(points, dtype=float))


def main():
    robot = Robot()
    saver = LidarSingleSaver(robot)
    saver.run_once_and_save()


if __name__ == "__main__":
    main()
