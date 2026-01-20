"""
Setup configuration for Job Alert Flask Application
"""

from setuptools import setup, find_packages
from pathlib import Path

# Read the contents of README file
this_directory = Path(__file__).parent
long_description = (this_directory / "README.md").read_text(encoding='utf-8')

# Read requirements from requirements.txt
requirements = []
requirements_path = this_directory / "requirements.txt"
if requirements_path.exists():
    with open(requirements_path, 'r', encoding='utf-8') as f:
        requirements = [line.strip() for line in f if line.strip() and not line.startswith('#')]

setup(
    name="job-alert",
    version="1.0.0",
    author="AI Kaptan",
    author_email="info@aikaptan.com",
    description="A modern Flask web application that monitors Google Jobs RSS feeds and displays product manager job opportunities",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://www.aikaptan.com/",
    project_urls={
        "Homepage": "https://www.aikaptan.com/",
        "Bug Reports": "https://github.com/aikaptan/job-alert/issues",
        "Source": "https://github.com/aikaptan/job-alert",
        "Documentation": "https://github.com/aikaptan/job-alert#readme",
    },
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Intended Audience :: End Users/Desktop",
        "Topic :: Internet :: WWW/HTTP :: Dynamic Content",
        "Topic :: Office/Business",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",
        "Framework :: Flask",
        "Operating System :: OS Independent",
        "Environment :: Web Environment",
    ],
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.0.0",
            "pytest-cov>=4.0.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
            "mypy>=1.0.0",
        ],
    },
    include_package_data=True,
    package_data={
        "": ["templates/*.html", "LICENSE", "README.md", "requirements.txt"],
    },
    entry_points={
        "console_scripts": [
            "job-alert=app:main",
        ],
    },
    py_modules=["app"],
    keywords=[
        "job-alert",
        "job-monitoring",
        "rss-feed",
        "product-manager",
        "flask",
        "google-jobs",
        "job-search",
        "automation",
        "web-scraping",
    ],
    license="MIT",
    zip_safe=False,
)
