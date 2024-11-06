import os
import xacro
from launch import LaunchDescription
from launch.actions import DeclareLaunchArgument, IncludeLaunchDescription
from launch_ros.actions import Node
from launch.substitutions import LaunchConfiguration
from launch.substitutions import Command
from launch.substitutions import FindExecutable
from launch.launch_description_sources import PythonLaunchDescriptionSource
from ament_index_python.packages import get_package_share_directory
import xacro

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


    # Process xacro file
    pkg_name = 'D435i'
    file_subpath = 'urdf/test_frame.urdf.xacro'
    xacro_file = os.path.join(get_package_share_directory(pkg_name), file_subpath)
    #robot_description_raw = xacro.process_file(xacro_file).toxml()
    robot_description_raw = Command([FindExecutable(name='xacro'), ' ', xacro_file, ' ', 'camera_name:=', LaunchConfiguration('')])

    # Configure the node 
    node_robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        name="robot_state_publisher",
        output='screen',
        parameters=[{'robot_description': robot_description_raw,
         'use_sim_time':True}]
    )

    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource([os.path.join(
            get_package_share_directory('gazebo_ros'), 'launch'), '/gazebo.launch.py']),
    )

    spawn_entity = Node(package='gazebo_ros', executable='spawn_entity.py',
        arguments=['-topic', 'robot_description',
                    '-entity', 'my_bot'],
        output='screen')

    return LaunchDescription([
        frame_id_arg,
        realsense_launch,
        node_robot_state_publisher,
        gazebo,
        spawn_entity
    ])
