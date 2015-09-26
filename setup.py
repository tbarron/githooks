from setuptools import setup
from githooks import version

setup(
    name='githooks',
    version=version.__version__,
    url='https://github.com/tbarron/githooks',
    license='',
    author='Tom Barron',
    author_email='tusculum@gmail.com',
    tests_require=['pytest'],
    description='git hooks to enforce versioning requirements',
    packages=['githooks'],
    entry_points = {'console_scripts':
                    ["gh = githooks:main"]
                    },
    )


