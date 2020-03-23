from setuptools import setup, find_packages

with open("README.md", "r") as f:
    long_description = f.read()

setup(
    name='rasa-storyteller',
    version='0.1',
    author="ezhvsalate",
    author_email="ezhvsalate@ya.ru",
    description="A simple GUI utility to create complex stories for RASA chatbots easily.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Ezhvsalate/rasa-storyteller",
    packages=find_packages(),
    python_requires=">=3.6",
    install_requires=[
        'PySimpleGUI==4.16.0',
        'markdown-generator==0.1.3',
        'PyYAML==5.3.1',
        'Pillow==7.0.0'
    ],
    entry_points='''
        [console_scripts]
        rasa-storyteller=gui.run:launcher
    ''',
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
