from setuptools import setup, find_packages

try:
    import pypandoc
    long_description = pypandoc.convert_file('README.md', 'rst')
except (IOError, ImportError):
    long_description = open('README.md').read()

setup(
    name='infection',
    version='1.0.0',
    packages=find_packages(exclude=("venv_win",)),
    description='Simulation model of disease infection in a population.',
    long_description=long_description,
    author='Underdoge',
    author_email='eduardo.chapa@gmail.com',
    url='https://github.com/Underdoge/infection',
    install_requires=[
        'argparse',
        'importlib-metadata; python_version == "3.6"',
    ],
)
