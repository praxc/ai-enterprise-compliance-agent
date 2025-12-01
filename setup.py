from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="ai-compliance-copilot",
    version="1.0.0",
    author="Praxc",
    author_email="praxc@github.com",
    description="Multi-agent AI system for automated compliance checking",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/praxc/ai-enterprise-compliance-agent",
    packages=find_packages(),
    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Libraries :: Python Modules",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.11",
    ],
    python_requires=">=3.11",
    install_requires=[
        "google-adk>=0.1.0",
        "google-generativeai>=0.8.0",
        "PyPDF2>=3.0.0",
    ],
    extras_require={
        "dev": [
            "pytest>=7.4.0",
            "pytest-asyncio>=0.21.0",
            "jupyter>=1.0.0",
        ],
    },
)