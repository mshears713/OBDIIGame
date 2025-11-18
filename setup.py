"""
Setup script for ECU Rogue - Modular Python Roguelike
"""

from setuptools import setup, find_packages
import pathlib

# Read the README file
here = pathlib.Path(__file__).parent.resolve()
long_description = (here / "README.md").read_text(encoding="utf-8")

# Read requirements
requirements = []
with open("requirements.txt") as f:
    requirements = [line.strip() for line in f if line.strip() and not line.startswith("#")]

setup(
    name="ecu-rogue",
    version="1.0.0",
    description="A modular Python roguelike game exploring automotive ECU systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/yourusername/OBDIIGame",
    author="Game Development Team",
    author_email="your.email@example.com",
    classifiers=[
        # Development status
        "Development Status :: 4 - Beta",

        # Intended audience
        "Intended Audience :: Education",
        "Intended Audience :: Developers",

        # Topics
        "Topic :: Games/Entertainment :: Role-Playing",
        "Topic :: Education",
        "Topic :: Software Development :: Libraries :: Python Modules",

        # License
        "License :: OSI Approved :: MIT License",

        # Python versions
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "Programming Language :: Python :: 3.12",

        # Operating systems
        "Operating System :: OS Independent",
    ],
    keywords="roguelike, game, education, ecu, automotive, procedural-generation, entity-component-system",
    packages=find_packages(exclude=["tests", "tests.*", "docs"]),
    python_requires=">=3.8",
    install_requires=requirements,
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-cov>=4.1.0",
            "mypy>=1.5.0",
            "black>=23.0.0",
            "flake8>=6.0.0",
        ],
    },
    package_data={
        "": [
            "config/**/*.json",
            "assets/**/*.txt",
            "assets/**/*.md",
        ],
    },
    include_package_data=True,
    entry_points={
        "console_scripts": [
            "ecu-rogue=main:main",
        ],
    },
    project_urls={
        "Bug Reports": "https://github.com/yourusername/OBDIIGame/issues",
        "Source": "https://github.com/yourusername/OBDIIGame",
        "Documentation": "https://github.com/yourusername/OBDIIGame/tree/main/docs",
    },
)
