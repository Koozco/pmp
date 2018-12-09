import setuptools
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()

setup(name='pmp',
      version='1.01.1',
      description='Python Multiwinner Package',
      url='https://github.com/Koozco/pmp',
      author='Katarzyna Banaszak, Bartosz Kusek',
      author_email='',
      license='?',
      packages=setuptools.find_packages(),
      install_requires=[
      ],
      zip_safe=False)

