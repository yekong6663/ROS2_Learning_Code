from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument,IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource

from launch_ros.actions import Node
from launch_ros.parameter_descriptions import ParameterValue

from launch.substitutions import LaunchConfiguration,Command

from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():

    default_package_path = get_package_share_directory('simulation')
    default_world_path = os.path.join(default_package_path, 'world', 'yozora_world', 'yozora_world.world')
    default_model_path = os.path.join(default_package_path, 'urdf', 'yozora_robot', 'yozora_robot.xacro')

    urdf_path_parameter = DeclareLaunchArgument(
        name='urdf_path',
        default_value=str(default_model_path),
        description='机器人的urdf文件的绝对路径'
    )

    command_urdf_content = Command(['xacro ', LaunchConfiguration('urdf_path')])

    urdf_content_parameter = ParameterValue(
        command_urdf_content,
        value_type=str
    )

    action_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        parameters=[{'robot_description': urdf_content_parameter}]
    )

    launch_gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            [get_package_share_directory('gazebo_ros'), '/launch', '/gazebo.launch.py']
        ),
        launch_arguments=[('world', default_world_path),('verbose','true')]
    )

    spawn_entity_node = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=[
            '-topic', '/robot_description',
            '-entity', 'yozora_robot',
        ]
    )
    
    return LaunchDescription([
            urdf_path_parameter,
            action_robot_state_publisher,
            launch_gazebo,
            spawn_entity_node
    ])