import os

from ament_index_python.packages import get_package_share_directory

from launch_ros.actions import Node
from launch import LaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch.actions import IncludeLaunchDescription, RegisterEventHandler

from launch.event_handlers import OnProcessExit

def generate_launch_description():
    pkg_share = get_package_share_directory('diff_bot')

    urdf_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(os.path.join(pkg_share, 'launch', 'urdf.launch.py'))
    )

    world_path = os.path.join(
        get_package_share_directory('gazebo_ros'),
        'launch',
        'gazebo.launch.py'
    )

    gazebo_world = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(world_path)
    )

    bot_args = [
    '-topic', 'robot_description', 
    '-entity', 'diff_bot'
    ]

    bot_spawn_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=bot_args,
        output='screen'
    )

    joint_state_broadcaster_node = Node(
        package='controller_manager',
        executable='spawner.py',
        arguments=['joint_state_broadcaster']
    )

    jsb_launch = RegisterEventHandler(
        event_handler=OnProcessExit(
            target_action=joint_state_broadcaster_node,
            on_exit=[bot_spawn_node],
        )
    )

    return LaunchDescription([
        urdf_launch,
        gazebo_world,
        jsb_launch,
        # joint_state_broadcaster_node,
    ])