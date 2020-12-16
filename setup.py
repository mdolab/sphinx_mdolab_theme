from setuptools import setup, find_packages
import re
from os import path

__version__ = re.findall(
    r"""__version__ = ["']+([0-9\.]*)["']+""",
    open("sphinx_mdolab_theme/__init__.py").read(),
)[0]

this_directory = path.abspath(path.dirname(__file__))
with open(path.join(this_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="sphinx_mdolab_theme",
    packages=find_packages(),
    version=__version__,
    license="MIT",
    description="MDO Lab sphinx theme",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="MDO Lab",
    author_email="mdolabbuildbot@gmail.com",
    url="https://github.com/mdolab/sphinx_mdolab_theme",
    keywords=["SPHINX", "THEME", "MDOLAB"],
    entry_points={
        "sphinx.html_themes": [
            "sphinx_mdolab_theme = sphinx_mdolab_theme",
        ]
    },
    package_data={
        "sphinx_mdolab_theme": [
            "theme.conf",
            "static/*.css",
        ]
    },
    include_package_data=True,
    install_requires=[
        "sphinx",
        "sphinx_rtd_theme",
        "pyyaml",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
