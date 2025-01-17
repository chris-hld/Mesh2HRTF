#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

with open('VERSION') as version_file:
    version = version_file.read().strip()

requirements = [
    'numpy>=1.14.0',
    'scipy>=1.5.0',
    'psutil',
    'sofar>=1.0.0',
    'pyfar>=0.5.3'
]

setup_requirements = ['pytest-runner', ]

test_requirements = [
    'pytest',
    'flake8'
]

setup(
    author="The mesh2hrtf developers",
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: EUPL 1.2'
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Programming Language :: Python :: 3.9'
    ],
    description="Numerical calculation of head-related transfer functions",
    install_requires=requirements,
    license="EUPL v1.2",
    long_description=readme,
    include_package_data=True,
    keywords='mesh2hrtf',
    name='mesh2hrtf',
    packages=find_packages(),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/mesh2hrtf',
    version=version,
    zip_safe=False,
    python_requires='>=3.7'
)
