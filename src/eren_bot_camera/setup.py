from setuptools import setup
import os
from glob import glob


package_name = 'eren_bot_camera'

setup(
    name=package_name,
    version='0.0.0',
    packages=[package_name],  # Modül adınızı burada eklediğinizden emin olun
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'), glob('launch/*.py')),

    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='eren',
    maintainer_email='eren@todo.todo',
    description='ROS2 package for hand tracking with camera using OpenCV and Mediapipe',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hand_tracking_node = eren_bot_camera.hand_tracking_node:main',

        ],
    },
)
