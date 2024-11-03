from setuptools import find_packages, setup

package_name = 'D435i'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        ('share/' + package_name + '/launch/', ['D435i/launch/d435i.launch.py']),
        ('share/' + package_name + '/urdf/', ['D435i/urdf/test_frame.urdf'])
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ors',
    maintainer_email='ors@todo.todo',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
        ],
    },
)
