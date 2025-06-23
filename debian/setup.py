from setuptools import setup, find_packages

setup(
    name='margarinawikidesktop',
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PySide6',
        'requests',
    ],
    entry_points={
        'gui_scripts': [
            'margarinawiki=margarinawikidesktop.margarina:start_app',
        ],
    },
)

