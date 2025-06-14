from setuptools import setup, find_packages

package_name = 'hewo_face'

setup(
    name=package_name,
    version='0.0.1',
    packages=find_packages(include=["hewo_face", "hewo_face.*"]),
    data_files=[
        ('share/ament_index/resource_index/packages', ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    package_data={
        'hewo_face': [
            'hewo/settings/**/*.yaml',
        ],
    },
    include_package_data=True,
    install_requires=[
        'setuptools',
        'pygame>=2.6.0',
        'numpy>=2.1.1',
        'screeninfo>=0.8.1',
        'opencv-python>=4.11.0.86',
        'Flask>=3.1.0',
        'PyYAML>=6.0.2',
        'requests>=2.32.3',
        'Werkzeug>=3.1.3',
        'scipy>=1.14.1',
        'click>=8.1.7'
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
