from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch.substitutions import LaunchConfiguration,Command

from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    default_package_path = get_package_share_directory('simulation')
    default_model_path = os.path.join(default_package_path, 'urdf', 'base_robot.xacro')

    xacro_path_parameter = DeclareLaunchArgument(
        name='xacro_path',
        default_value=str(default_model_path),
        description='机器人的xacro文件的绝对路径'
    )

    command_xacro_content = Command(['xacro ', LaunchConfiguration('xacro_path')])

    xacro_content_parameter = ParameterValue(
        command_xacro_content,
        value_type=str
    )

    action_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': xacro_content_parameter}]
    )

    action_joint_state_publisher = Node(
        package='joint_state_publisher',
        executable='joint_state_publisher',
    )

    rviz2 = Node(
        package='rviz2',
        executable='rviz2',
        arguments=['-d', os.path.join(default_package_path, 'config', 'rviz2_config_xacro.rviz')]
    )
    
    return LaunchDescription([
            xacro_path_parameter,
            action_robot_state_publisher,
            action_joint_state_publisher,
            rviz2
    ])