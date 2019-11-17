import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name='bayesian_networks',
    version='0.8',
    author="bkbilly",
    author_email="bkbilly@hotmail.com",
    description="Implementation for bayesian network with Enumeration, Rejection Sampling and Likelihood Weighting",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/bkbilly/bayesian_networks",
    packages=setuptools.find_packages(),
    install_requires=[
        'pytz>=2019.2',
        'matplotlib>=3.0.3',
        'networkx>=2.4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
