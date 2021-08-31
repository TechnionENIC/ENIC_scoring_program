import setuptools


setuptools.setup(
    name="ENIC_gradings",
    version = "0.1",
    author="Victoria Khalfin Fekson",
    author_email="skhalfin@campus.technion.ac.il",
    install_requires=['pyreadstat','lxml','beautifulsoup4','pandas'],
    classifiers=(
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ),
)
