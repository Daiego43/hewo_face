from setuptools import setup, find_packages

# Leer el archivo de requirements.txt
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

setup(
    name='hewo_pygame',
    version='0.1.0',
    description='A Pygame project for modular game elements with reusable objects.',
    author='Diego Delgado Chaves, Daiego43',
    author_email='diedelcha@gmail.com',
    packages=find_packages(include=['game',
                                    'game.main',
                                    'game.objects',
                                    'game.objects.*',
                                    'game.resources.*',
                                    'game.settings',
                                    'game.settings.*',]),
    install_requires=requirements,
    package_data={
        'hewo_pygame.game.settings.hewo': ['*.yaml'],  # Incluye los archivos de configuración YAML
        'hewo_pygame.game.settings.window': ['*.yaml'],  # Incluye los archivos de configuración YAML
        'hewo_pygame.game.resources': ['resources/*'],  # Incluye recursos adicionales
    },
    entry_points={
        'console_scripts': [
            'hewo_game=game.main.window:main',  # Ajuste para invocar desde línea de comandos
        ],
    },
    classifiers=[
        'Programming Language :: Python :: 3.10',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
    ],
    python_requires='>=3.10',
)
