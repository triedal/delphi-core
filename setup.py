import setuptools

setuptools.setup(
    name="dcore",
    version="0.1.0",
    url="https://github.com/triedal/delphi-core.git",

    author="Tyler Riedal",
    author_email="riedalsolutions@gmail.com",

    description="Core for delphi AV software",
    long_description=open('README.rst').read(),

    packages=setuptools.find_packages(),

    install_requires=[
        'appdirs',
        'astroid',
        'backports.functools-lru-cache',
        'click',
        'configparser',
        'enum34',
        'future',
        'isort',
        'lazy-object-proxy',
        'mccabe',
        'MySQL-python',
        'numpy',
        'packaging',
        'pandas',
        'pefile',
        'psycopg2',
        'py',
        'pylint',
        'pyparsing',
        'pytest',
        'python-dateutil',
        'pytz',
        'PyYAML',
        'scikit-learn',
        'scipy',
        'singledispatch',
        'six',
        'SQLAlchemy',
        'tqdm',
        'wrapt'
    ],

    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
    ],
    entry_points={
        'console_scripts': [
            'dcore = delphi_core.cli:cli'
        ]
    }
)
