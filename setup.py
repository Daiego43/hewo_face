from setuptools import setup, find_packages

package_name = 'hewo_face_ros'

setup(
    name=package_name,
    version='1.0.0',
    packages=find_packages(include=["hewo_face", "hewo_face.*"]),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    include_package_data=True,
    install_requires=[
        'hewo_face>=2.6.0',
    ],
    zip_safe=True,
    maintainer='Diego Delgado Chaves',
    maintainer_email='diedelcha@gmail.com',
    description='A Pygame project for modular game elements with reusable objects. Used for HeWo face control.',
    license='MIT',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            'hewo_main_node = hewo_face.nodes.main_node:main'
        ],
    },
)
