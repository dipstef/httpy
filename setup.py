from distutils.core import setup

VERSION = '0.1'

desc = """Http domain and error classes and http-header parsing."""

name = 'httpy'

setup(name=name,
      version=VERSION,
      author='Stefano Dipierro',
      author_email='dipstef@github.com',
      url='http://github.com/dipstef/{}/'.format(name),
      description='Utilities and decorators for function execution',
      license='http://www.apache.org/licenses/LICENSE-2.0',
      packages=['httpy', 'httpy.headers'],
      platforms=['Any'],
      long_description=desc,
      requires=['collected', 'connected']
)