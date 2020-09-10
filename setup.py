from setuptools import setup

setup(
    name="sphinx_mdolab_theme",
    packages=["sphinx_mdolab_theme"],
    version="0.1",
    license="MIT",
    description="MDO Lab sphinx theme",
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
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",  # Chose either "3 - Alpha", "4 - Beta" or "5 - Production/Stable" as the current state of your package
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Build Tools",
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3",
    ],
)
