from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import os

def generate_launch_description():
    # eren_bot_description/gazebo.launch.py dosyasını dahil etme
    eren_bot_description_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(
                get_package_share_directory('eren_bot_description'),
                'launch',
                'gazebo.launch.py'
            )
        )
    )

    # eren_bot_camera/hand_tracking_node çalıştırma
    hand_tracking_node = Node(
        package='eren_bot_camera',
        executable='hand_tracking_node',
        name='hand_tracking_node',
        output='screen'
    )

    return LaunchDescription([
        eren_bot_description_launch,
        hand_tracking_node
    ])
