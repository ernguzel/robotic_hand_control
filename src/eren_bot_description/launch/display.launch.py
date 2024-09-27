from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
   

    eren_bot_description_dir = get_package_share_directory('eren_bot_description')
    
    # xacro dosyasının tam yolunu oluştur
    xacro_file = os.path.join(eren_bot_description_dir, 'urdf', 'eren_bot.xacro')

    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=xacro_file,
        description="URDF dosyasinin doğru yolu"
    )

    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]), 
        value_type=str
    )

    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    # joint_state_publisher_gui = Node(
    #     package="joint_state_publisher_gui",
    #     executable="joint_state_publisher_gui"
    # )

    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen", 
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        # joint_state_publisher_gui,
        rviz_node
    ])