from setuptools import find_packages, setup

package_name = 'motor_package'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools', 'numpy', 'pygame'],
    zip_safe=True,
    maintainer='root',
    maintainer_email='drnd@nd.edu',
    description='TODO: Package description',
    license='TODO: License declaration',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'jetsonTalker = motor_package.jetson_talker:main',
            'joystickTalker = motor_package.joystick_talker:main'
        ],
    },
)
