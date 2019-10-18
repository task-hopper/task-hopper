#!/user/bin/python

from setuptools import setup

__author__ = 'Josh Crank, Michael Buckley, Jarrett Drouillard'

dependencies = [
    'argparse'
]

entry_points = {
    'console_scripts': [
        'hop = hop.__main__:main'
    ]
}

setup(
    name='hop',
    version='0.0.1',
    description='A project management cli',
    author='Josh Crank, Michael Buckley, Jarrett Drouillard',
    author_email='joshuatcrank@gmail.com, jarrett@thestyl.us',
    license='GNU',
    url='https://github.com/task-hopper/task-hopper',
    install_requires=dependencies,
    include_package_data=True,
    packages=['hop'],
    entry_points=entry_points
)

