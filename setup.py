
import os
import pkg_resources
from setuptools import setup, find_packages

setup(
    name="podcast-agent",
    py_modules=[],
    version="0.0.1",
    description="AI Agent that monitors podcasts and finds clips of interest",
    readme="README.md",
    python_requires=">=3.8",
    author="Jonathan McCoy",
    url="https://github.com/jonmc12/podcast-agent",
    license="MIT",
    packages=find_packages(exclude=["tests*"]),
    install_requires=[
        str(r)
        for r in pkg_resources.parse_requirements(
            open(os.path.join(os.path.dirname(__file__), "requirements.txt"))
        )
    ],
    entry_points = {},
    include_package_data=True,
    extras_require={},
)