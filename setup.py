from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="rasa-storyteller",
    version="0.2.1",
    author="ezhvsalate",
    author_email="ezhvsalate@ya.ru",
    description="A simple GUI utility to create complex stories for RASA chatbots easily.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ezhvsalate/rasa-storyteller",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        "PySimpleGUI==4.22.0",
        "AnyTree==2.8.0",
        "markdown-generator==0.1.3",
        "PyYAML==5.3.1",
        "Pillow==8.2.0",
    ],
    entry_points="""
        [console_scripts]
        rasa-storyteller=gui.run:launcher
    """,
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
