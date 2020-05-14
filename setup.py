# -*- coding: utf-8 -*-
from setuptools import find_packages
from setuptools import setup
from os.path import dirname, abspath, join
from os import linesep

version = "1.0.0.dev0"


def read(filename):
    with open(join(abspath(dirname(__file__)), filename), 'r') as f:
        return f.read()

def readfiles(*args):
    return (2*linesep).join(map(read, args))


setup(
    name="collective.ploneqrcode",
    version=version,
    description="ploneqrcode",
    long_description=readfiles('README.rst',
                               'CONTRIBUTORS.rst',
                               'CHANGES.rst'),
    # Get more strings from
    # https://pypi.python.org/pypi?:action=list_classifiers
    classifiers=[
        "Framework :: Plone",
        "Framework :: Plone :: 4.3",
        "Programming Language :: Python",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ],
    keywords="plone qrcode pil pillow image",
    author="Cleber J Santos",
    author_email="cleber@cleberjsantos.com.br",
    license="GPL",
    packages=find_packages(exclude=["ez_setup"]),
    namespace_packages=["collective"],
    include_package_data=True,
    zip_safe=False,
    install_requires=[
        "setuptools",
        "pyqrcode",
        "plone.api",
        "plone.memoize",
    ],
    extras_require={
        "test": [
            "plone.app.testing",
            "unittest2",
            "robotsuite",
            "robotframework-selenium2library",
            "plone.app.robotframework",
            "robotframework-debuglibrary",
        ]
    },
    entry_points="""
    # -*- Entry points: -*-

    [z3c.autoinclude.plugin]
    target = plone
    """,
)
