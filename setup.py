import os
from setuptools import setup, find_packages
from pip.req import parse_requirements
from pip.download import PipSession

version = '0.1.0'

def read(f):
    return open(os.path.join(os.path.dirname(__file__), f)).read().strip()

install_reqs = parse_requirements('requirements.txt', session=PipSession())
reqs = [str(ir.req) for ir in install_reqs]

setup(name='fractalprojection',
      version=version,
      description=('Runs a "fractal projection" that psysal mentioned, to project earth a strange way.'),
      long_description='\n\n'.join((read('README.md'), read('CHANGELOG'))),
      classifiers=[
          'License :: OSI Approved :: MIT License',
          'Intended Audience :: Other Audience',
          'Programming Language :: Python :: 3'],
      author='K.C.Saff',
      author_email='kc@saff.net',
      url='https://github.com/kcsaff/fractalprojection',
      license='MIT',
      packages=find_packages(),
      install_requires=reqs,
      entry_points={
          'console_scripts': ['fractalprojection = fractalprojection:entry']
      },
      include_package_data = True,
      package_data={'fractalprojection.resources.': ['*.jpg', '*.md', '*.html']}
)
