from setuptools import find_packages
from setuptools import setup

setup(
    name='ddd',
    version='0.1.0',
    author='Pavel V. Pristupa',
    author_email='pristupa@gmail.com',
    packages=find_packages(exclude=['tests*']),
    scripts=[],
    url='https://github.com/pristupa/ddd',
    license='MIT',
    description='Domain-Driven Design for Python',
    long_description=open('README.md').read(),
    install_requires=[
        'dataclasses == 0.6',
    ],
    python_requires=">=3.6",
)
