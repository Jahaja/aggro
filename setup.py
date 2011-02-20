# coding=UTF-8
from setuptools import setup, find_packages

version = '0.1'

setup(
    name='aggro',
    version=version,
    description="Python feed aggregator",
    long_description="""Aggro is a simple asynchronous feed aggregator using gevent""",
    classifiers=[
        "Topic :: Internet :: WWW/HTTP :: Syndication",
        "Development Status :: 4 - Beta",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Intended Audience :: Developers",
        "Intended Audience :: System Administrators",
    ],
    keywords='',
    author='Joakim Hamrén',
    author_email='',
    url='',
    license='MIT',
    packages=find_packages(exclude=['ez_setup', 'examples', 'tests']),
    include_package_data=True,
    zip_safe=False,
    install_requires=[],
)
