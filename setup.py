import setuptools

with open("README.md", "r", encoding="utf-8") as fhand:
    long_description = fhand.read()

setuptools.setup(
    name="itunes-tlk",
    version="0.0.1",
    author="Antoine Clais",
    author_email="antoine@math-clais.ovh",
    description=("An over-simplified downloader package to "
                "demonstrate python module and tool packaging."),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sialcant/itunes-tlk",
    project_urls={
        "Bug Tracker": "https://github.com/Sialcant/itunes-tlk/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    install_requires=["requests"],
    packages=setuptools.find_packages(),
    python_requires=">=3.6",
    entry_points={
        "console_scripts": [
            "download = downloader.cli:main",
        ]
    }
)