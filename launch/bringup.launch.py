"""
Top-level launch file.
Starts Gazebo simulation + Nav2 (with AMCL localisation) together.

Usage:
  ros2 launch 4wd_robot bringup.launch.py
  ros2 launch 4wd_robot bringup.launch.py map:=/path/to/your_map.yaml
"""
import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    TimerAction,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration


def generate_launch_description():
    pkg_share = get_package_share_directory('4wd_robot')

    use_sim_time = LaunchConfiguration('use_sim_time', default='true')
    map_file     = LaunchConfiguration('map')
    x_pose       = LaunchConfiguration('x_pose', default='0.0')
    y_pose       = LaunchConfiguration('y_pose', default='0.0')

    # ── Gazebo + robot ────────────────────────────────────────────────────────
    sim_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(pkg_share, 'launch', 'sim.launch.py')
        ),
        launch_arguments={
            'use_sim_time': use_sim_time,
            'x_pose':       x_pose,
            'y_pose':       y_pose,
        }.items(),
    )

    # ── Nav2 (planner + controller + BT + waypoint follower) ─────────────────
    # Delayed by 5 s to give Gazebo time to finish spawning the robot.
    nav2_launch = TimerAction(
        period=5.0,
        actions=[
            IncludeLaunchDescription(
                PythonLaunchDescriptionSource(
                    os.path.join(pkg_share, 'launch', 'navigation.launch.py')
                ),
                launch_arguments={
                    'map':          map_file,
                    'use_sim_time': use_sim_time,
                }.items(),
            )
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument(
            'use_sim_time',
            default_value='true',
            description='Use simulation clock'),

        DeclareLaunchArgument(
            'map',
            default_value=os.path.join(pkg_share, 'maps', 'obstacle_map.yaml'),
            description='Full path to map yaml file to load for navigation'),

        DeclareLaunchArgument(
            'x_pose', default_value='0.0',
            description='Initial X position of the robot in Gazebo'),

        DeclareLaunchArgument(
            'y_pose', default_value='0.0',
            description='Initial Y position of the robot in Gazebo'),

        sim_launch,
        nav2_launch,
    ])
