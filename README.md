# 4WD Robot Workspace

## Visualizing Navigation

### Demo
<video src="assets/demo.webm" controls autoplay muted loop width="100%"></video>

To visualize the robot navigating, run the following commands. 

1. Launch the Gazebo simulation:
   ```bash
   ros2 launch my_robot_bringup my_robot_gazebo.launch.xml
   ```

2. In another terminal, launch the navigation stack:
   ```bash
   ros2 launch my_robot_bringup navigation.launch.xml
   ```
