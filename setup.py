import os
from setuptools import find_packages
from setuptools import setup

here = os.path.abspath(os.path.dirname(__file__))
about = {}
with open(os.path.join(here, 'ddd', '__version__.py')) as f:
    exec(f.read(), about)


def read_requirements(req_file):
    with open(os.path.join('requirements', req_file)) as req:
        return [line.strip() for line in req.readlines() if line.strip() and not line.strip().startswith('#')]


requirements = read_requirements('base.txt')

setup(
    name='py-ddd',
    packages=find_packages(exclude=['tests*']),
    include_package_data=True,
    version=about['__version__'],
    description='Domain-Driven Design framework for Python',
    url='https://github.com/pristupa/ddd',
    author='Pavel V. Pristupa',
    author_email='pristupa@gmail.com',
    license='MIT',
    install_requires=requirements,
    classifiers=[
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Development Status :: 3 - Alpha',
        'Operating System :: OS Independent',
        'Environment :: Web Environment',
        'Programming Language :: Python',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Software Development :: Libraries :: Application Frameworks',
    ],
)
