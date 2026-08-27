from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

with open("requirements.txt", "r", encoding="utf-8") as fh:
    requirements = [line.strip() for line in fh if line.strip() and not line.startswith("#")]

setup(
    name="cybernet-agent",
    version="0.1.0",
    author="Ghayoor Hafeez",
    author_email="ghayoor@example.com",
    description="An intelligent autonomous agent for cybersecurity monitoring and threat detection",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghayoorhafeez/cybernet-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.9",
    install_requires=requirements,
    entry_points={
        "console_scripts": [
            "cybernet-agent=src.main:main",
        ],
    },
)
