import os

from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import (
    DeclareLaunchArgument,
    IncludeLaunchDescription,
    ExecuteProcess,
)
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node


def generate_launch_description():
    pkg_share = get_package_share_directory('4wd_robot')
    gazebo_ros_share = get_package_share_directory('gazebo_ros')

    world_file = os.path.join(pkg_share, 'worlds', 'obstacles.world')
    urdf_file  = os.path.join(pkg_share, 'urdf', 'robot.urdf.xacro')

    use_sim_time  = LaunchConfiguration('use_sim_time',  default='true')
    x_pose        = LaunchConfiguration('x_pose',        default='0.0')
    y_pose        = LaunchConfiguration('y_pose',        default='0.0')

    robot_description = Command(['xacro ', urdf_file])

    # ── Gazebo server ────────────────────────────────────────────────────────
    gzserver = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gzserver.launch.py')
        ),
        launch_arguments={'world': world_file, 'verbose': 'false'}.items(),
    )

    # ── Gazebo client (GUI) ──────────────────────────────────────────────────
    gzclient = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(gazebo_ros_share, 'launch', 'gzclient.launch.py')
        ),
    )

    # ── Robot State Publisher ────────────────────────────────────────────────
    rsp = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{
            'use_sim_time': use_sim_time,
            'robot_description': robot_description,
        }],
    )

    # ── Spawn robot entity in Gazebo ─────────────────────────────────────────
    spawn_entity = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        name='spawn_entity',
        output='screen',
        arguments=[
            '-topic', 'robot_description',
            '-entity', '4wd_robot',
            '-x', x_pose,
            '-y', y_pose,
            '-z', '0.1',
        ],
    )

    return LaunchDescription([
        DeclareLaunchArgument('use_sim_time', default_value='true',
                              description='Use simulation clock'),
        DeclareLaunchArgument('x_pose', default_value='0.0',
                              description='Initial X position of the robot'),
        DeclareLaunchArgument('y_pose', default_value='0.0',
                              description='Initial Y position of the robot'),

        gzserver,
        gzclient,
        rsp,
        spawn_entity,
    ])
