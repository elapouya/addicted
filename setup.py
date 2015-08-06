from setuptools import setup
import os

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

setup(name='addicted',
      version='0.0.4',
      description='addict ExtendeD',
      long_description=long_description,
      classifiers=[
          "Intended Audience :: Developers",
          "Development Status :: 2 - Pre-Alpha",
          "Programming Language :: Python :: 2",
          "Programming Language :: Python :: 2.7",
      ],
      keywords='attribute, AttrDict, addict',
      url='https://github.com/elapouya/addicted',
      author='Eric Lapouyade',
      author_email='elapouya@gmail.com',
      license='LGPL 2.1',
      packages=['addicted'],
      install_requires = ['noattr'],
      eager_resources = [],
      zip_safe=False)
