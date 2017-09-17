from setuptools import setup, find_packages
import os
from osuapi import __version__ as version, __title__ as name, __author__ as author, __license__ as license
import pypandoc


def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

with open('README.md') as readme_md:
    readme = pypandoc.convert_text(readme_md.read(), 'rst', 'markdown')

setup(
    name=name,
    version=version,
    author=author,
    url="https://github.com/khazhyk/osuapi",
    license="MIT",
    long_description=readme,
    keywords="osu",
    packages=find_packages(),
    description="osu! api wrapper.",
    classifiers=[
      "Development Status :: 1 - Planning",
      "Intended Audience :: Developers",
      "License :: OSI Approved :: MIT License",
      "Topic :: Utilities"
    ]
)
