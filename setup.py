import setuptools
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pmp',
      version='1.2.2',
      description='Python Multiwinner Package',
      url='https://github.com/Koozco/pmp',
      author='Katarzyna Banaszak, Bartosz Kusek',
      author_email='',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=['pytest', 'six', 'numpy'],
      zip_safe=False)
