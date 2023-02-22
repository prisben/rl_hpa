from setuptools import setup

setup(name='gym_env',
      version='0.0.2',
      install_requires=['gym','requests','kubernetes==v23.6.0']  # And any other dependencies foo needs
      #dependency_links=['http://github.com/kubernetes-client/repo/tarball/master#egg=python-12.0.0-snapshot']
)