# 4WD Robot — Autonomous Navigation in Gazebo

A ROS 2 package for a **four-wheel drive (skid-steer) robot** that can navigate autonomously inside a Gazebo simulation using **Nav2** and **AMCL** localisation.

---

## Package Layout

```
4wd_robot/
├── urdf/
│   ├── robot.urdf.xacro        # Top-level URDF (includes all parts)
│   ├── robot_core.xacro        # Chassis + 4 wheels + inertia macros
│   ├── lidar.xacro             # 2-D laser scanner + Gazebo ray plugin
│   ├── imu.xacro               # IMU link + Gazebo IMU plugin
│   └── gazebo_control.xacro    # Skid-steer drive plugin + wheel friction
├── config/
│   └── nav2_params.yaml        # Nav2 + AMCL parameters
├── launch/
│   ├── bringup.launch.py       # All-in-one: Gazebo + Nav2 (recommended)
│   ├── sim.launch.py           # Gazebo only
│   ├── navigation.launch.py    # Nav2 (full stack)
│   ├── localization.launch.py  # AMCL localisation only
│   └── robot_state_publisher.launch.py
├── worlds/
│   └── obstacles.world         # Walled arena with 4 obstacles
└── maps/
    ├── obstacle_map.yaml        # Map metadata
    └── obstacle_map.pgm         # Pre-built occupancy grid
```

---

## Prerequisites

| Requirement | Version |
|-------------|---------|
| ROS 2       | Humble / Iron |
| Gazebo      | Classic (11) |
| Nav2        | matching ROS 2 distro |

Install Nav2 and Gazebo dependencies:

```bash
sudo apt install \
  ros-$ROS_DISTRO-nav2-bringup \
  ros-$ROS_DISTRO-navigation2 \
  ros-$ROS_DISTRO-gazebo-ros-pkgs \
  ros-$ROS_DISTRO-xacro \
  ros-$ROS_DISTRO-joint-state-publisher
```

---

## Build

```bash
cd ~/ros2_ws/src
# Copy / symlink this package here, then:
cd ~/ros2_ws
colcon build --packages-select 4wd_robot
source install/setup.bash
```

---

## Run

### Full autonomous demo (Gazebo + Nav2 + AMCL)

```bash
ros2 launch 4wd_robot bringup.launch.py
```

This single command:
1. Starts **Gazebo** with the obstacle world and spawns the 4WD robot.
2. Launches **robot_state_publisher** to broadcast TF frames.
3. After a 5-second delay, starts the **Nav2** stack (map server, AMCL, planner, controller, BT navigator, etc.).

### Send a navigation goal

Open **RViz 2**, add the *Nav2 Goal* tool, and click anywhere on the map — the robot will plan and execute the path autonomously.

From the command line:

```bash
ros2 action send_goal /navigate_to_pose nav2_msgs/action/NavigateToPose \
  "pose: {header: {frame_id: map}, pose: {position: {x: 3.0, y: 1.0, z: 0.0}, orientation: {w: 1.0}}}"
```

### Use your own map

```bash
ros2 launch 4wd_robot bringup.launch.py map:=/path/to/your_map.yaml
```

### Simulation only (no Nav2)

```bash
ros2 launch 4wd_robot sim.launch.py
```

Then drive with:

```bash
ros2 topic pub /cmd_vel geometry_msgs/msg/Twist \
  "{linear: {x: 0.2}, angular: {z: 0.0}}" --once
```

### AMCL localisation only

```bash
ros2 launch 4wd_robot localization.launch.py map:=/path/to/your_map.yaml
```

---

## Robot Specifications

| Property | Value |
|----------|-------|
| Drive type | Skid-steer (4WD) |
| Chassis | 40 × 30 × 10 cm |
| Wheel radius | 7 cm |
| Sensor | 360° 2-D LiDAR (10 Hz, 10 m range) |
| IMU | 100 Hz |
| Max linear velocity | 0.5 m/s |
| Max angular velocity | 2.0 rad/s |

---

## Saving a New Map with SLAM

If you want to build a new map instead of using the bundled one:

```bash
# Terminal 1 – start simulation
ros2 launch 4wd_robot sim.launch.py

# Terminal 2 – SLAM Toolbox (install separately if needed)
ros2 launch slam_toolbox online_async_launch.py use_sim_time:=true

# Drive the robot around, then save:
ros2 run nav2_map_server map_saver_cli -f ~/my_map

# Use the saved map:
ros2 launch 4wd_robot bringup.launch.py map:=~/my_map.yaml
```
