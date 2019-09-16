from pip.download import PipSession
from pip.req import parse_requirements
from setuptools import find_packages
from setuptools import setup

import PySELibrary as project

setup(
    name=project.APP_NAME,
    version=project.VERSION,
    description=project.DESCRIPTION,
    keywords=project.KEYWORDS,
    long_description=project.LONG_DESCRIPTION,
    author=project.AUTHOR_NAME,
    author_email=project.AUTHOR_EMAIL,
    url=project.URL,
    license=project.LICENSE,
    packages=find_packages(),
    install_requires=[str(x.req) for x in
                      parse_requirements('requirements.txt', session=PipSession())],
    classifiers=["Development Status :: 1 - Beta",
                 "Intended Audience :: Developers",
                 "License :: OSI Approved :: GNU General Public License v3",
                 "Programming Language :: Python",
                 "Programming Language :: Python :: 2.7",
                 'Programming Language :: Python :: 3',
                 'Programming Language :: Python :: 3.5',
                 'Programming Language :: Python :: 3.6',
                 "Topic :: Software Development :: Libraries :: Python Modules",
                 ],
)
