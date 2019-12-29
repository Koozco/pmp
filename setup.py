import setuptools
from setuptools import setup


def readme():
    with open('README.md') as f:
        return f.read()


setup(name='pmp',
      version='1.3.0',
      description='Python Multiwinner Package',
      url='https://github.com/Koozco/pmp',
      download_url='https://github.com/Koozco/pmp/archive/v1.3.0.tar.gz',
      author='Katarzyna Banaszak, Bartosz Kusek',
      author_email='kussy.kusy@gmail.com',
      license='MIT',
      packages=setuptools.find_packages(),
      install_requires=['pytest', 'six', 'numpy'],
      zip_safe=False)
