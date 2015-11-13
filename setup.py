from setuptools import setup, find_packages
import sys
from zephyr import __version__
import os

def include_path(datas, path):
    for root, dirs, files in os.walk(path):
        base, ex = path.split(os.path.sep, 1)
        for f in files:
            name, ext = f.split('.')
            if ext in ('css', 'js', 'html', 'ico', 'png', 'gif'):
                datas.append(os.path.join(ex, f))
        for d in dirs:
            include_path(datas, os.path.join(path, d))


def _package_data():
    datas = []
    path = os.path.join(os.path.dirname(__file__), 'zephyr')
    include_path(datas, os.path.join(path, 'asset'))
    include_path(datas ,os.path.join(path, 'view'))
    return datas

setup(
    name = 'zephyr',
    version = __version__,
    author = "Thomas",
    author_email='lyanghwy@gmail.com',
    description = "A Blog Cms backed by Tornado&MySQL in Python",
    license = "http://www.apache.org/licenses/LICENSE-2.0",
    keywords = "A Blog Cms backed by Tornado&MySQL in Python",
    url='https://github.com/whiteclover/Zephyr',
    long_description=open('README.rst').read(),
    packages=find_packages(exclude=['t', 't.*']),
    zip_safe=False,
    include_package_data=True,
    package_data = {
        # Non-.py files to distribute as part of each package
        'zephyr': _package_data()
    },
    install_requires = ['setuptools', 'tornado', 'markdown', 'Jinja2', 'dbpy', 'pillow', 'redis'],
    test_suite='unittests',
    classifiers=(
        "Development Status :: Production/Alpha",
        "License :: Apache Software License",
        "Natural Language :: English",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.7",
        "Topic :: Blog Cms"
        )
    )
