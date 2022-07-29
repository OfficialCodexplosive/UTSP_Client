import os
import setuptools  # type: ignore

dir_path = os.path.dirname(os.path.realpath(__file__))
with open(os.path.join(dir_path, "requirements.txt")) as f:
    required_packages = f.read().splitlines()
with open(os.path.join(dir_path, "README.md"), "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="UTSP client",
    version="0.1.0",
    author="Noah Pflugradt",
    author_email="n.pflugradt@fz-juelich.de",
    description="Universal Time Series Provider Client",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/FZJ-IEK3-VSA/tsib",
    include_package_data=True,
    packages=setuptools.find_packages(),
    install_requires=required_packages,
    setup_requires=["setuptools-git"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: End Users/Server",
        "Intended Audience :: Science/Research",
        "License :: OSI Approved :: MIT License",
        "Natural Language :: English",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.8",
        "Topic :: Scientific/Engineering",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords=["buildings", "thermal load", "electricity load"],
)