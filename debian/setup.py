from setuptools import setup, find_packages

setup(
    name='PestoWiki'
    version='1.0',
    packages=find_packages(),
    install_requires=[
        'PySide6',
        'requests',
    ],
    entry_points={
        'gui_scripts': [
            'pestowiki=pestowiki.margarina:start_app',
        ],
    },
)

