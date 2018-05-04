#!/usr/bin/env python
from subprocess import check_call

from setuptools import setup, find_packages, Command
from pyqt_distutils.build_ui import build_ui


class BuildResourcesCommand(build_ui):
    """Builds UI and resources."""

    def run(self):
        # build UI & resources
        build_ui.run(self)


class BuildAppCommand(Command):
    """Builds the application. """

    description = 'Builds the application.'
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        command = ['pyinstaller', '-y', 'app.spec']
        self.run_command('build_res')
        self.announce('Running command: %s' % ' '.join(map(str, command)))
        check_call(command)


setup(name='poe-run-helper',
      version='0.0.1',
      packages=find_packages(),
      description='PoE Run Helper',
      author='JooHee Lee',
      author_email='hello@joohee.me',
      license='MIT',
      url='https://github.com/jl24/poe-run-helper',
      entry_points={
          'gui_scripts': ['app=app.__main__:main'],
      },
      cmdclass={
          'build_res': BuildResourcesCommand,
          'build_app': BuildAppCommand,
      })
