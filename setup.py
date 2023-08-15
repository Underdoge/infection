""" This module is used to create the infection distribution package.
"""
from setuptools import setup

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='infection',
    version='1.0.0',
    description='Simulation Model of a Disease spreading throughout a \
population.',
    long_description=long_description,
    author='Eduardo Chapa (Underdoge)',
    author_email='eduardo.chapa@gmail.com',
    url='https://github.com/Underdoge/infection',
    install_requires=[
        'importlib-metadata; python_version == "3.7+"',
    ],
)