from setuptools import setup
import os
import re

def read(*names):
    values = dict()
    for name in names:
        filename = name + '.rst'
        if os.path.isfile(filename):
            fd = open(filename)
            value = fd.read()
            fd.close()
        else:
            value = ''
        values[name] = value
    return values


long_description = """
%(README)s

News
====
%(CHANGES)s
""" % read('README', 'CHANGES')

def get_version(pkg):
    path = os.path.join(os.path.dirname(__file__),pkg,'__init__.py')
    with open(path) as fh:
        m = re.search(r'^__version__\s*=\s*[\'"]([^\'"]+)[\'"]',fh.read(),re.M)
    if m:
        return m.group(1)
    raise RuntimeError("Unable to find __version__ string in %s." % path)

setup(name='addicted',
      version=get_version('addicted'),
      description='addict ExtendeD',
      long_description=long_description,
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 4 - Beta",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='attribute AttrDict addict addicted textops naghelp',
      url='https://github.com/elapouya/addicted',
      author='Eric Lapouyade',
      author_email='elapouya@gmail.com',
      license='LGPL 2.1',
      packages=['addicted'],
      install_requires = ['noattr'],
      eager_resources = [],
      zip_safe=False)
