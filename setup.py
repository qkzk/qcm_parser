import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="qcm_parser",
    version="0.1.3",
    author="qkzk",
    author_email="qu3nt1n@gmail.com",
    description="A parser of QCM file",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/qkzk/qcm_parser",
    project_urls={
        "Bug Tracker": "https://github.com/qkzk/qcm_parser/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: GNU General Public License v2 (GPLv2)",
        "Operating System :: OS Independent",
    ],
    package_dir={"": "src"},
    packages=setuptools.find_packages(where="src"),
    install_requires=[
        "markdown",
    ],
    python_requires=">=3.6",
)
