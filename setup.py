#!/usr/bin/env python3
"""
MarketDataAPI CLI Setup

Install this package to get the 'marketdata' command globally available.
Run: pip install -e .
Then use: marketdata instruments list
"""

from setuptools import setup, find_packages

setup(
    name="marketdata-api-cli",
    version="1.0.0",
    description="Professional CLI for MarketDataAPI",
    packages=find_packages(),
    entry_points={
        'console_scripts': [
            'marketdata=marketdata_cli:main',
            'mapi=marketdata_cli:main',  # Short alias
        ],
    },
    install_requires=[
        'click>=8.0.0',
        'rich>=13.0.0',
        'sqlalchemy',
        'requests',
    ],
    python_requires='>=3.8',
)
