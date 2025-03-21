import os
import xacro
from launch import LaunchDescription
from launch.substitutions import LaunchConfiguration, Command
from launch_ros.actions import Node
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Load the package directory
    pkg_share = get_package_share_directory('diff_bot')

    # Load the URDF file
    urdf = os.path.join(pkg_share, 'description', 'diff_bot.urdf.xacro')
    doc = xacro.process_file(urdf)
    robot_description_config = doc.toxml()

    # Nodes
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name='robot_state_publisher',
        output='screen',
        parameters=[{'robot_description': robot_description_config}]
    )

    rviz = Node(
        package='rviz2',
        executable='rviz2',
        name='rviz2',
        output='screen',
        arguments=['-d', os.path.join(pkg_share, 'config', 'rviz', 'urdf.rviz')]
    )

    joint_state_publisher = Node(
        package='joint_state_publisher_gui',
        executable='joint_state_publisher_gui',
        name='joint_state_publisher',
        output='screen',
        parameters=[]
    )

    # Launch!
    return LaunchDescription([
        robot_state_publisher,
        rviz,
        # joint_state_publisher
    ])
