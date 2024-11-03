import os
import xacro
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory

def generate_launch_description():
    # Creating launch argument for Frame ID to associate depth camera data
    frame_id_arg = DeclareLaunchArgument(
        'frame_id',
        default_value='camera',
        description='Frame ID to associate with the depth camera'
    )

    # Path to the RealSense launch file
    realsense_launch_file = os.path.join(
        get_package_share_directory('realsense2_camera'),
        'launch',
        'rs_launch.py'
    )

    # Include RealSense launch file with frame_id param
    realsense_launch = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(realsense_launch_file),
        launch_arguments={
            #'base_frame_id': LaunchConfiguration('frame_id'),
            # 'depth_frame_id': LaunchConfiguration('frame_id')
            'camera_name': LaunchConfiguration('frame_id')
        }.items()
    )

    # Need to test this with test_frame.urdf
    urdf_file = os.path.join(
        get_package_share_directory('D435i'),
        'urdf',
        'test_frame.urdf'
    )

    # Configure the node 
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name="robot_state_publisher",
        output='screen',
        parameters=[{'robot_description': open(urdf_file).read(), 'use_sim_time':True}]
    )

    return LaunchDescription([
        frame_id_arg,
        realsense_launch,
        node_robot_state_publisher
    ])
