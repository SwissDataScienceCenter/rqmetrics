from pathlib import Path
from setuptools import setup

long_description = Path("README.md").read_text()

requirements = [
    "rq>=1.2.2",
    "redis>=3.5.3",
    "prometheus_client>=0.8.0",
]

tests_require = [
    "fakeredis==1.4.1",
    "pytest==5.4.2",
    "requests>=2.23.0",
    "black==19.10b0"
]


extras_require = {
    'docs': [
        'Jinja2>=2.10.1',
        'Sphinx>=1.6.3',
        'renku-sphinx-theme>=0.1.0',
    ],
    'runner': ['cwlref-runner>=1.0', ],
    'notebook': [],
    'sentry': ['sentry-sdk>=0.7.4', ],
    'tests': tests_require,
}

setup_requires = [
    'pytest-runner>=2.6.2',
    'setuptools_scm>=3.1.0',
]

extras_require['all'] = list(setup_requires)

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
    tests_require=tests_require,
    extras_require=extras_require,
    setup_requires=requirements + setup_requires,
    packages=["rqexport"],
    classifiers=[
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: Apache Software License',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
        'Development Status :: 4 - Beta',
        'Monitoring'
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["rqexport = __main__:main"]},
)
