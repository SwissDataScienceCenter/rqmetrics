import os.path
from pathlib import Path
from setuptools import setup
from pipenv.project import Project
from pipenv.utils import convert_deps_to_pip

project_file = Project(chdir=False).parsed_pipfile
cwd = os.path.abspath(os.path.dirname(__file__))


long_description = Path("README.md").read_text()

requirements = convert_deps_to_pip(project_file["packages"], r=False)
test_requirements = convert_deps_to_pip(project_file["dev-packages"], r=False)

setup(
    name="rq-prometheus-exporter",
    url="https://github.com/SwissDataScienceCenter/rq-prometheus-exporter",
    license="",
    version="",
    author="",
    author_email="",
    description="",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=requirements,
    packages=["rqexport"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Monitoring",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["rqexport = core.__main__:main"]},
)
