#!/usr/bin/env python3
"""
MarketDataAPI - Professional Financial Market Data Platform

A comprehensive platform for managing and analyzing financial market data
including instruments, transparency calculations, legal entities, and more.
"""

from setuptools import setup, find_packages
import os

# Read README file
def read_file(filename):
    """Read a file and return its contents."""
    try:
        with open(os.path.join(os.path.dirname(__file__), filename), 'r', encoding='utf-8') as f:
            return f.read()
    except FileNotFoundError:
        return ""

# Read requirements from requirements.txt
def read_requirements():
    """Read requirements from requirements.txt."""
    requirements = []
    try:
        with open('requirements.txt', 'r') as f:
            requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]
    except FileNotFoundError:
        # Fallback to minimal requirements
        requirements = [
            'PyYAML>=6.0.1',
            'pandas>=2.0.0',
            'SQLAlchemy>=2.0.0',
            'Flask>=2.3.0',
            'flask-cors>=4.0.0',
            'python-dotenv>=1.0.0',
            'requests>=2.31.0',
            'aiohttp>=3.9.0',
            'alembic>=1.12.0',
            'tenacity>=8.2.0',
            'dicttoxml==1.7.16',
            'flask-restx>=1.1.0',
            'beautifulsoup4>=4.12.0',
            'lxml>=4.9.0',
            'tqdm>=4.66.0',
            'click>=8.0.0',
            'rich>=13.0.0',
            'setuptools>=65.0.0'
        ]
    return requirements

setup(
    name="marketdata-api",
    version="1.0.5",
    author="Robin Jonsson",
    author_email="robin_j88@hotmail.com",  # Update with your email
    description="Professional Financial Market Data Platform with CLI and API",
    long_description=read_file("README.md"),
    long_description_content_type="text/markdown",
    url="https://github.com/RobiinJonsson/MarketDataAPI",  # Update with your repo URL
    packages=find_packages(where="src"),
    package_dir={"": "src"},
    include_package_data=True,
    zip_safe=False,
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Financial and Insurance Industry",
        "Intended Audience :: Developers",
        "Topic :: Office/Business :: Financial",
        "Topic :: Database",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Operating System :: OS Independent",
    ],
    entry_points={
        'console_scripts': [
            'marketdata=marketdata_api.cli:main',
            'mapi=marketdata_api.cli:main',
        ],
    },
    install_requires=read_requirements(),
    extras_require={
        'dev': [
            'pytest>=7.4.0',
            'pytest-cov>=4.1.0',
            'black>=23.0.0',
            'isort>=5.12.0',
            'flake8>=6.0.0',
            'mypy>=1.5.0',
        ],
        'docs': [
            'sphinx>=7.0.0',
            'sphinx-rtd-theme>=1.3.0',
        ],
        'sqlserver': [
            'pyodbc>=5.2.0',
        ]
    },
    python_requires='>=3.8',
    keywords='finance, market-data, transparency, mifid, esma, firds, fitrs, cli, api',
    project_urls={
        'Bug Reports': 'https://github.com/RobiinJonsson/MarketDataAPI/issues',
        'Source': 'https://github.com/RobiinJonsson/MarketDataAPI',
        'Documentation': 'https://github.com/RobiinJonsson/MarketDataAPI/docs',
    },
)
