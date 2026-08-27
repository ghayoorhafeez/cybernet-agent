from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="cybernet-nbb-ai",
    version="0.1.0",
    author="Ghayoor Hafeez",
    author_email="ghayoor@example.com",
    description="AI Voice Operator for Cybernet NBB Portal",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ghayoorhafeez/cybernet-agent",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
    ],
    python_requires=">=3.11",
    entry_points={
        "console_scripts": [
            "cybernet-ai=src.main:main",
        ],
    },
)
