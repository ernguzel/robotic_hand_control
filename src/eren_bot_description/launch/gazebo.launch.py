from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
import os
from ament_index_python.packages import get_package_share_directory
from launch_ros.parameter_descriptions import ParameterValue
from launch.substitutions import Command, LaunchConfiguration

def generate_launch_description():
    # Get the directory of the description package
    eren_bot_description_dir = get_package_share_directory('eren_bot_description')
    
    # xacro file path
    xacro_file = os.path.join(eren_bot_description_dir, 'urdf', 'eren_bot.xacro')

    # Gazebo world file path (optional, default Gazebo empty world is used if not provided)
    world_file = os.path.join(get_package_share_directory('eren_bot_description'), 'worlds', 'worlds.world')


    # Declare model argument for xacro file
    model_arg = DeclareLaunchArgument(
        name="model",
        default_value=xacro_file,
        description="URDF dosyasının doğru yolu"
    )

    # Create robot description parameter
    robot_description = ParameterValue(
        Command(["xacro ", LaunchConfiguration("model")]), 
        value_type=str
    )

    # Node to publish robot description to /robot_description
    robot_state_publisher = Node(
        package="robot_state_publisher",
        executable="robot_state_publisher",
        parameters=[{"robot_description": robot_description}]
    )

    # Node to spawn the robot into Gazebo
    spawn_entity = Node(
        package="gazebo_ros",
        executable="spawn_entity.py",
        arguments=["-topic", "/robot_description", "-entity", "eren_bot"],
        output="screen"
    )

    # Include Gazebo launch file to start Gazebo with verbose mode
    gazebo_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        ),
        launch_arguments={'world': world_file, 'verbose': 'true'}.items()  # Optional, only needed if using a custom world file
    )

    # RViz Node (optional, can be disabled if only using Gazebo)
    rviz_node = Node(
        package="rviz2",
        executable="rviz2",
        name="rviz2",
        output="screen"
    )

    return LaunchDescription([
        model_arg,
        robot_state_publisher,
        spawn_entity,  # Add the robot to Gazebo
        gazebo_launch,  # Start Gazebo with verbose logging enabled
        rviz_node  # Start RViz (optional)
    ])
