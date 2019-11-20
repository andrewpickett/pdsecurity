import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="pdsecurity",
    version="0.0.3",
    author="Andrew J. Pickett",
    author_email="picketta@gmail.com",
    description="Simple package containing basic security classes/code for bcrypt and JWT auth",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/andrewpickett/pdsecurity",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)
