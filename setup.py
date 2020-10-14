import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="BatchScript",
    version="0.0.8",
    author="TaylorHere",
    author_email="taylorherelee@gmail.com",
    description="Python Master-Queue-Worker Structure multiple task tool",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/TaylorHere/BatchScript",
    packages=setuptools.find_packages(),
    include_package_data=True,
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
    ],
)
