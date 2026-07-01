from setuptools import find_packages, setup

package_name = '3_python_turtle_feedback_control'

setup(
    name=package_name,
    version='0.0.0',
    packages=find_packages(exclude=['test']),
    data_files=[
        ('share/ament_index/resource_index/packages',
            ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='ros',
    maintainer_email='744311194@qq.com',
    description='TODO: Package description',
    license='Apache_2.0',
    extras_require={
        'test': [
            'pytest',
        ],
    },
    entry_points={
        'console_scripts': [
            "turtlesim_feedback_control = 3_python_turtle_feedback_control.turtlesim_feedback_control:main",
        ],
    },
)
